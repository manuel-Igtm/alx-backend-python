from django.test import TestCase
from .models import User, Message, Notification

class NotificationSignalTest(TestCase):
    def test_notification_created_on_message(self):
        sender = User.objects.create_user(username='sender', password='test123')
        receiver = User.objects.create_user(username='receiver', password='test123')
        msg = Message.objects.create(sender=sender, receiver=receiver, content='Hello!')
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.first().user, receiver)
