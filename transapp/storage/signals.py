from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from storage.models import Action
from .constants import StatusChoice
from core.models import WorkPosition

@receiver(post_save, sender=Action)
def my_callback(sender, instance, created, **kwargs):
    if instance.status == StatusChoice.DELIVERED_BROKEN and created:
        print(reverse('storage:action-complain-email', args=[instance.pk])) # brak możliwości dodania wiadomości do responsa

@receiver(m2m_changed, sender=Action.workers.through)
def check_workers_position(sender, instance, action, *args, **kwargs):
    if action=="pre_add":
        xd = [worker.position==WorkPosition.WAREHOUSER for worker in instance.workers.all()]
        return all(xd)
