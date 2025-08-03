from django.db.models.signals import post_save, pre_save ,post_delete
from django.dispatch import receiver
from .models import Message, Notification,MessageHistory,User

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def save_message_history(sender, instance, **kwargs):
    if instance.pk:  # Only run if updating an existing message
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            # Save the old content to history
            MessageHistory.objects.create(
                message=old_message,
                previous_content=old_message.content
            )
            instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Related messages and notifications are deleted via CASCADE
    # MessageHistory will be deleted through related messages
    print(f"Cleaned up data for user {instance.username}")
