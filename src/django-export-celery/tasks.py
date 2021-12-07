from datetime import datetime

from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from celery import shared_task
from import_export.formats.base_formats import DEFAULT_FORMATS

import statuses
from .models import ExportJob


@shared_task(bind=False)
def execute_export_job(
        job_id,
        app_label,
        model_name,
        resource,
        send_email,
        email,
        site,
        file_content_type,
        filename,
        ids,
        **kwargs):

    job = ExportJob.objects.get(pk=job_id)
    job.status = statuses.PENDING
    job.save()

    try:
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        model = content_type.model_class()
        queryset = model.objects.filter(pk__in=ids)
        extra_data = kwargs.get('send_celery_data')
        file_format = list(filter(lambda f: f.CONTENT_TYPE == file_content_type, DEFAULT_FORMATS))[0]()
        resource_class = model.get_export_resources()[resource][1]
        resource = resource_class()

        if hasattr(resource, 'handle_resource_kwargs') and callable(getattr(resource, 'handle_resource_kwargs')):
            resource.on_celery_handle_resource_data(extra_data)

        data = resource.export(queryset)
        serialized = file_format.export_data(data)

        if not file_format.is_binary():
            serialized = serialized.encode('utf8')
        job.file.save(filename, ContentFile(serialized))

        if send_email:
            _app_label = ExportJob._meta.app_label
            _model_name = ExportJob._meta.model_name

            file_link = site + reverse('admin:%s_%s_changelist' % (_app_label, _model_name)) + f"?id={job.pk}"
            send_mail(
                'Export Job Completed',
                (
                    'Your export job is completed. \n'
                    'The file can be downloaded at:\n\n'
                    f'{file_link}'
                ),
                None,
                [email],
            )

        job.completed_on = datetime.now()
        job.status = statuses.SUCCESS

    except Exception as e:
        job.status = statuses.FAILURE
        if send_email:
            send_mail(
                'Export job failed',
                f'Your export job on {app_label} failed.',
                None,
                [email],
            )
        raise e
    finally:
        job.save()

    return
