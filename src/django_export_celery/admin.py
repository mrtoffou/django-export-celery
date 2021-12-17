from django.contrib import admin

import models
from .urls import urlpatterns


@admin.register(models.ExportJob)
class ExportJobAdmin(admin.ModelAdmin):
    list_display = (
        'model',
        'resource',
        'status',
        'file_download',
        'file_size',
        'author',
        'started_on',
        'completed_on',
    )
    list_filter = (
        'status',
        'model',
        'resource',
    )

    def get_urls(self):
        return urlpatterns + super().get_urls()

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
