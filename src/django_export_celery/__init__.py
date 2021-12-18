from django.conf import settings

settings.DJANGO_EXPORT_CELERY_UPLOAD_TO = getattr(
    settings,
    'DJANGO_EXPORT_CELERY_UPLOAD_TO',
    'django-export-celery-jobs/',
)

settings.DJANGO_EXPORT_CELERY_ENABLE_EMAIL = getattr(
    settings,
    'DJANGO_EXPORT_CELERY_ENABLE_EMAIL',
    False,
)
