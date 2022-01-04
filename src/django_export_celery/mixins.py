import json

from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from import_export.admin import ExportMixin
from . import statuses, tasks, forms, models


def is_jsonable(val):
    try:
        json.dumps(val)
        return True
    except (TypeError, OverflowError):
        return False


class ExportCeleryMixin(ExportMixin):

    export_form = None
    send_celery_data = dict()

    def on_celery_send_data(self, **kwargs):
        for key, value in kwargs.items():
            if not is_jsonable(value):
                raise Exception(f"{value} is not jsonable")

        return self.send_celery_data.update(kwargs)

    def get_export_form(self, form, request, *args, **kwargs):
        pass

    def export_action(self, request, *args, **kwargs):
        if not self.has_export_permission(request):
            raise PermissionDenied

        formats = self.get_export_formats()
        self.export_form = forms.ExportJobForm(formats, request.POST or None)
        self.export_form.set_default_resource_choices(
            [(key, val[0]) for key, val in self.model.get_export_resources().items()]
        )
        self.get_export_form(self.export_form, request, *args, **kwargs)

        if self.export_form.is_valid():
            file_format = formats[int(self.export_form.cleaned_data['file_format'])]()
            content_type = file_format.get_content_type()
            queryset = self.get_export_queryset(request)
            filename = self.get_export_filename(request, queryset, file_format)
            resource = request.POST.get('resource')
            send_email = True if 'send_email' in request.POST else False
            ids = queryset.values_list('id', flat=True)
            model_name = self.model._meta.model_name
            app_label = self.model._meta.app_label
            site = "{}://{}".format(request.scheme, get_current_site(request))
            # resource_label = self.model.get_export_resources()[resource][0]

            job = models.ExportJob.objects.create(
                status=statuses.STARTED,
                resource=self.model.get_export_resources()[resource][0],
                model=model_name,
                author=request.user.id,
            )

            if not hasattr(settings, 'CELERY_BROKER_URL'):
                messages.set_level(request, messages.WARNING)
                messages.warning(request, "CELERY_BROKER_URL is not defined")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            tasks.execute_export_job.delay(
                job.id,
                app_label,
                model_name,
                resource,
                send_email,
                request.user.email,
                site,
                content_type,
                filename,
                list(ids),
                send_celery_data=self.send_celery_data,
            )

            messages.set_level(request, messages.INFO)
            if send_email and request.user.email:
                messages.info(
                    request,
                    f"Your export job is in progress.\n"
                    f"An email with a file link will be sent when completed."
                )
            else:
                messages.info(request, f"Your export job is in progress.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        context = self.get_export_context_data()

        context.update(self.admin_site.each_context(request))

        context['title'] = _("Export")
        context['form'] = self.export_form
        context['opts'] = self.model._meta
        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.export_template_name], context)
