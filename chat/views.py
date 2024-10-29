from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatThread, ChatMessage
from .utils import create_chat_chain, generate_thread_id
from django.http import StreamingHttpResponse
import json
from django.views.generic import TemplateView


# Create your views here.
class StartChatView(APIView):
    def post(self, request):
        asset_id = request.data.get("asset_id")
        if not asset_id:
            return Response(
                {"error": "Asset ID is required"}, status.HTTP_400_BAD_REQUEST
            )

        thread_id = generate_thread_id()
        ChatThread.objects.create(thread_id=thread_id, asset_id=asset_id)

        return Response({"thread_id": thread_id}, status.HTTP_201_CREATED)


class ChatMessageView(APIView):
    def post(self, request):
        thread_id = request.data.get("thread_id")
        user_message = request.data.get("user_message")

        if not thread_id or not user_message:
            return Response(
                {"error": "Thread ID and message are required"},
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            thread = ChatThread.objects.get(thread_id=thread_id)
        except ChatThread.DoesNotExist:
            return Response({"error": "Invalid thread ID"}, status.HTTP_404_NOT_FOUND)

        # save user message
        ChatMessage.objects.create(thread=thread, content=user_message, is_user=True)

        # get chat chain
        chain = create_chat_chain(thread.asset_id)
        if chain is None:
            return Response(
                {"error": "Unable to create chat chain. No documents found."},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # stream the response
        def stream_response():
            response = ""
            for chunk in chain.stream({"question": user_message}):
                # print(f"Chunk: {chunk}")
                if "answer" in chunk:
                    response += chunk["answer"]
                    yield f"data: {json.dumps({'content': chunk['answer']})}\n\n"

                # if "source_documents" in chunk:
                #     print("Source Documents: ", chunk["source_documents"])

            # save the generate message
            ChatMessage.objects.create(thread=thread, content=response, is_user=False)

            yield "data: [DONE]\n\n"

        return StreamingHttpResponse(
            stream_response(), content_type="text/event-stream"
        )


class ChatHistoryView(APIView):
    def get(self, request):
        thread_id = request.query_params.get("thread_id")
        if not thread_id:
            return Response(
                {"error": "Thread ID is required"}, status.HTTP_400_BAD_REQUEST
            )

        try:
            thread = ChatThread.objects.get(thread_id=thread_id)
        except ChatThread.DoesNotExist:
            return Response({"error": "Invalid thread ID"}, status.HTTP_404_NOT_FOUND)

        messages = ChatMessage.objects.filter(thread=thread).values(
            "content", "is_user", "timestamp"
        )
        return Response(messages, status.HTTP_200_OK)


class ChatView(TemplateView):
    template_name = "chat/index.html"
