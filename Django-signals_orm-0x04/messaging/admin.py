from django.contrib import admin
from .models import User, Message, Notification,MessageHistory

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(MessageHistory)