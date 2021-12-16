Overview
===

django-export-celery is a Django application that enables long processing exports using `celery` and `django-import-export`


Dependencies
===
Python (3.7, 3.8, 3.9)

Packages
```text
Django==3.2
celery==5.2.0
django-import-export==2.3.0
django-author==1.0.2
```

Installation and Configuration
===
Celery must be setup before starting. \
Please refer to [Using Celery with Django](https://docs.celeryproject.org/en/v5.2.0/django/first-steps-with-django.html) for more information.

Install with `pip`
```
pip install django-export-celery
```

Add apps to `INSTALLED_APPS` and `MIDDLEWARE` to project settings.
```python
# settings.py
INSTALLED_APPS = (
    ...
    'import_export',
    'author',
    'django_export_celery',
)

MIDDLEWARE = (
    ...
    'author.middlewares.AuthorDefaultBackendMiddleware,
)
```


How to use
===

1. Setup `resources`
```python
# apps/resources.py
from .models import Animal
from import_export import resources


class DogResource(resources.ModelResource):
    class Meta:
        model = Animal
```

2. Setup export resources to `model`
```python
# apps/models.py
from django.db import models


class Animal(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    @staticmethod
    def get_export_resources():
        from .resources import DogResource
        return {
            'dog_rsc': ('Dog', DogResource),
        }
```

3. Add `ExportCeleryMixin` to `admin.py`
```python
# apps/admin.py
from django.contrib import admin
from .models import Animal
from django_export_celery.mixins import ExportCeleryMixin


@admin.register(Animal)
class AnimalAdmin(ExportCeleryMixin, admin.ModelAdmin):
    list_display = (
        'name',
    )
```


Demo App
===
`./project/` contains the necessary files to start a sample project

To get started
```
cd project
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

Known Issues
===
* Does not respect ordering when exporting
* Export to certain file types will break 
* Admin views that inherit mixins from `import_export.mixins` with `django_export_celery.mixins` may cause issues


Issue Tracker
===
If you have any bugs, suggestions, or compliants please report an issue [here](https://github.com/mrtoffou/django-export-celery/issues)


References
===
* https://www.djangoproject.com/
* https://github.com/django-import-export/django-import-export
* https://docs.celeryproject.org/en/stable/getting-started/introduction.html
* https://github.com/lambdalisue/django-author
