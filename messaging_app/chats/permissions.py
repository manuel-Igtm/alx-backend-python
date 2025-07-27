from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to access, send, update, or delete messages in that conversation.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Assumes obj is a Message or Conversation instance with a 'conversation' attribute
        participants = obj.conversation.participants.all()
        return request.user in participants