from django.urls import path

from .views import download_file

urlpatterns = [
    path(
        r'<str:pk>/download-file/',
        download_file,
        name='django_export_celery_exportjob_download_file'
    ),
]
