from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participant_ids')
        if not participant_ids or len(participant_ids) < 2:
            return Response({"error": "At least two participants are required."}, status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() < 2:
            return Response({"error": "Invalid participants."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related('sender', 'conversation')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    
    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')
        sender_id = request.user.user_id if request.user.is_authenticated else None

        if not all([conversation_id, message_body, sender_id]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = User.objects.get(user_id=sender_id)
        except (Conversation.DoesNotExist, User.DoesNotExist):
            return Response({"error": "Invalid conversation or sender."}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant of this conversation."}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(conversation=conversation, sender=sender, message_body=message_body)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({"error": "You are not allowed to update this message."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({"error": "You are not allowed to delete this message."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
@login_required
@cache_page(60)  # Cache this view for 60 seconds
def user_threaded_conversations(request):
    user = request.user
    messages = Message.objects.filter(sender=request.user).select_related('receiver', 'sender', 'edited_by').prefetch_related('replies')

    def build_thread(msg):
        return {
            'id': str(msg.message_id),
            'content': msg.content,
            'receiver': msg.receiver.username,
            'timestamp': msg.timestamp,
            'edited': msg.edited,
            'replies': [build_thread(reply) for reply in msg.replies.all()]
        }

    threads = [build_thread(msg) for msg in messages if msg.parent_message is None]
    return JsonResponse({'threads': threads}, safe=False)
