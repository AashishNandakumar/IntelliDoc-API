from .celery import app as celery_app

__all__ = ("celery_app",)  # include celery in __all__ namespace
