import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CryptoPriceAnalysis.settings')

app = Celery('CryptoPriceAnalysis', broker='redis://localhost:6379/2', include=['PriceAnalysis.tasks'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY2')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch_coin_price': {
        'task': "PriceAnalysis.tasks.fetch_coin_price",
        'schedule': 60.0,
        'args': ()
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


