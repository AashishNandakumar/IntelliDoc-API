from rest_framework import serializers


class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def validate_file(self, value):
        if value.content_type not in [
            "text/plain",
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]:
            raise serializers.ValidationError(
                "Unsupported file type. Please upload a .txt, .pdf, .doc or .docx file"
            )
        return value
