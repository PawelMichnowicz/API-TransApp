from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from storage.models import Action
from .constants import StatusChoice


@receiver(post_save, sender=Action)
def my_callback(sender, instance, created, **kwargs):
    if instance.status == StatusChoice.DELIVERED_BROKEN and created:
        print(reverse('storage:action-complain-email', args=[instance.pk]))
