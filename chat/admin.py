from django.contrib import admin
from .models import ChatMessage, ChatThread

# Register your models here.
admin.site.register(ChatMessage)
admin.site.register(ChatThread)
