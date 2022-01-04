from django.conf import settings

settings.DJANGO_EXPORT_CELERY_ENABLE_EMAIL = getattr(
    settings,
    'DJANGO_EXPORT_CELERY_ENABLE_EMAIL',
    True,
)
