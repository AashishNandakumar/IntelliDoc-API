from celery import shared_task
from .utils import process_document
from django.core.files.storage import default_storage


@shared_task
def process_document_task(file_path):
    asset_id = process_document(file_path)
    default_storage.delete(file_path)
    print(f"asset id: {asset_id}")
    return asset_id
