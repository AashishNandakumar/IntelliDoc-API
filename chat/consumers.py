import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import create_chat_chain
from .models import ChatThread, ChatMessage
from asgiref.sync import (
    sync_to_async,
)  # takes a blocking/synchronous function and makes it work in async code (hey don't block everything else while you work)


class ChatConsumer(AsyncWebsocketConsumer):
    # called when a new WebSocket connection is established
    async def connect(self):
        self.thread_id = self.scope["url_route"]["kwargs"]["thread_id"]
        self.room_group_name = f"chat_{self.thread_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    # called when a WebSocket connction is closed
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # called with a decoded WebSocket frame
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        thread = await sync_to_async(ChatThread.objects.get)(thread_id=self.thread_id)
        chain = await sync_to_async(create_chat_chain)(thread.asset_id)

        if chain is None:
            await self.send(
                text_data=json.dumps(
                    {"error": "Unable to create chain. No document found"}
                )
            )

        result = await sync_to_async(chain)({"question": message})
        answer = result["answer"]

        await sync_to_async(ChatMessage.objects.create)(
            thread=thread,
            content=message,
            is_user=True,
        )

        await sync_to_async(ChatMessage.objects.create)(
            thread=thread,
            content=answer,
            is_user=False,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": answer,
            },
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )
