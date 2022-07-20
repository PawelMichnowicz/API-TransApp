from celery import Celery

from providers.factory import create_provider


celery = Celery(__name__)
celery.conf.broker_url = "redis://redis:6379/0"


@celery.task
def provider_send(provider_name, sender, recipent, text):
    provider = create_provider(provider_name, sender, recipent)
    return provider.send(text)

