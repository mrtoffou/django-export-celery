# Generated by Django 3.1.4 on 2021-11-16 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to='django-export-celery-jobs')),
                ('status', models.CharField(choices=[('SUCCESS', 'SUCCESS'), ('PENDING', 'PENDING'), ('FAILURE', 'FAILURE'), ('STARTED', 'STARTED')], default=None, max_length=25, null=True)),
                ('model', models.CharField(default='', max_length=255)),
                ('resource', models.CharField(default='', max_length=255)),
                ('started_on', models.DateTimeField(auto_now_add=True)),
                ('completed_on', models.DateTimeField(blank=True, default=None, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exportjob_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exportjob_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
        ),
    ]
