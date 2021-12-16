Overview
===

django-export-celery is a Django application 

Requirements
===
Python >= 3.6

Dependencies
```text
Django==3.2
celery==5.2.0
django-import-export==2.2.0
django-author==1.0.2 
```

Installation and Configuration
===
Celery must be setup prior to starting. \
Please refer to [Using Celery with Django](https://docs.celeryproject.org/en/v5.2.0/django/first-steps-with-django.html) for more information

1. Add app to `INSTALLED_APPS` 
```python
# settings.py
INSTALLED_APPS = (
    ...
    'author',
    'django_export_celery',
)
```
2. Add to `MIDDLEWARE`
```python
# settings.py
MIDDLEWARE = (
    ...
    'author.middlewares.AuthorDefaultBackendMiddleware,
)
```

Example App
===

To get started, run the following commands:
```
cd project
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

Known Issues:
===

- Does not respect ordering filter on export
- Exports to some file types will break