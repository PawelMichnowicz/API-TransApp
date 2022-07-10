from celery import Celery
from time import sleep



celery = Celery(__name__)
celery.conf.broker_url = "redis://redis:6379/0"

@celery.task
def reverse(text):
    sleep(5)
    return text[::-1]