from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
import os
from django.conf import settings

from .tasks import process_document_task
from processor.utils import process_document
from .serializers import DocumentUploadSerializer


# Create your views here.
class DocumentProcessView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # file_obj = request.FILES.get("file")
        # if not file_obj:
        #     return Response({"error": "No file provided"}, status.HTTP_400_BAD_REQUEST)

        serializer = DocumentUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file_obj = serializer.validated_data["file"]

        # save the file temporarily
        file_path = default_storage.save(f"tmp/{file_obj.name}", file_obj)
        file_path = os.path.join(settings.MEDIA_ROOT, file_path)

        try:
            # # process the document
            # asset_id = process_document(file_path)

            # # delete the temporary file
            # default_storage.delete(file_path)

            task = process_document_task.delay(file_path)

            return Response({"task_id": task.id}, status.HTTP_200_OK)
        except Exception as e:
            # delete the temporary file in case of error
            default_storage.delete(file_path)
            return Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
