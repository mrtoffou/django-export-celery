import os

from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe


class ExportJob(models.Model):
    file = models.FileField(upload_to='django-export-celery-jobs/', blank=False, null=False, max_length=255)
    status = models.CharField(max_length=25, null=True, default='')
    model = models.CharField(max_length=255, default='')
    resource = models.CharField(max_length=255, default='')
    started_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(default=None, null=True, blank=True)
    author = models.ForeignKey(
        blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='exportjob_create',
        to=settings.AUTH_USER_MODEL, verbose_name='author'
    )

    class Meta:
        verbose_name_plural = 'Export Jobs'

    def file_size(self):
        try:
            return f'{self.file.size/1000} kB' if self.file else ''
        except FileNotFoundError:
            return 'N/A'

    def file_download(self):
        if self.file:
            return mark_safe('<a href="{}/download-file/">{}</a>'.format(self.pk, os.path.basename(self.file.name)))


@receiver(post_delete, sender=ExportJob)
def remove_file(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)
