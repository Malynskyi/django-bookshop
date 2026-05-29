import os

from celery import Celery


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "db_django_proj.settings.production",
)

app = Celery("db_django_proj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()