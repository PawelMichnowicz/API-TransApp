"""
Signals for storage APIs
"""
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import Q
from core.constants import WorkPosition

from storage.models import Action


@receiver(m2m_changed, sender=Action.workers.through)
def check_workers_position(sender, instance, action, *args, **kwargs):
    ''' Signal that check if all workers in warehouse have warehouser position '''
    if action=="pre_add":
        return instance.workers.all().filter(~Q(position=WorkPosition.WAREHOUSER)).exists()

