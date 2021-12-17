from django.contrib import admin
from .models import Question, Choice
from import_export.admin import ImportExportMixin
from django_export_celery.mixins import ExportCeleryMixin


@admin.register(Question)
class QuestionAdmin(ImportExportMixin, ExportCeleryMixin, admin.ModelAdmin):
    list_display = (
        'question_text',
        'pub_date',
    )


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'choice_text',
        'votes',
    )
