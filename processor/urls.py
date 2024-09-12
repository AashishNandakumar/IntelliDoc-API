from django.urls import path
from .views import DocumentProcessView

urlpatterns = [
    path("documents/process/", DocumentProcessView.as_view(), name="process_document"),
]
