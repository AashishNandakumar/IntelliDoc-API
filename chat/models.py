from django.db import models


# Create your models here.
class ChatThread(models.Model):
    thread_id = models.CharField(max_length=255, unique=True)
    asset_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    thread = models.ForeignKey(
        ChatThread, related_name="messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    is_user = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
