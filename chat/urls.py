from django.urls import path
from .views import *

urlpatterns = [
    path("start/", StartChatView.as_view(), name="start_chat"),
    path("message/", ChatMessageView.as_view(), name="chat_message"),
    path("history/", ChatHistoryView.as_view(), name="chat_history"),
]
