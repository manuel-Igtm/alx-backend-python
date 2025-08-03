from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from .models import Message
from django.core.serializers import serialize

User = get_user_model()

@csrf_exempt
@login_required
def delete_user(request):
    if request.method == 'DELETE':
        user = request.user
        username = user.username
        user.delete()
        return JsonResponse({'message': f'User {username} and related data deleted successfully.'})
    return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)

@login_required
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

@login_required
def unread_messages(request):
    unread = Message.unread.unread_for_user(request.user).only('message_id', 'sender', 'content', 'timestamp')
    data = [
        {
            'id': str(msg.message_id),
            'sender': msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp
        }
        for msg in unread
    ]
    return JsonResponse({'unread': data})

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

...

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
