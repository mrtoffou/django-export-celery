from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import ExportJob


@login_required
@permission_required('django_export_celery.view_exportjob', raise_exception=True)
@require_http_methods(["GET"])
def download_file(request, *args, **kwargs):
    pk = kwargs.get('pk')
    try:
        job = ExportJob.objects.get(pk=pk)
        if job.file:
            filename = job.file.name.split('/')[-1]
            response = HttpResponse(job.file, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename

            return response
    except (ExportJob.DoesNotExist, FileNotFoundError):
        messages.warning(request, 'File cannot be found.')
        return redirect('/admin/django_export_celery/exportjob/')
