import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_commance.settings")

app = Celery("e_commance")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
