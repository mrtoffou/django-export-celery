from django import forms

from import_export.forms import ExportForm
from django.conf import settings


class ExportJobForm(ExportForm):
    resource = forms.ChoiceField(choices=(), label='Export Resource')

    if settings.DJANGO_EXPORT_CELERY_ENABLE_EMAIL:
        send_email = forms.BooleanField(initial=True, required=False, label='Send email on completion')

    def set_default_resource_choices(self, choices):
        self.fields['resource'].choices = choices
