"""
Signals for storage APIs
"""
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from core.constants import WorkPosition

from storage.models import Action


@receiver(m2m_changed, sender=Action.workers.through)
def check_workers_position(sender, instance, action, *args, **kwargs):
    ''' Signal that check if all workers in warehouse have warehouser position '''
    if action=="pre_add":
        is_warehouser = [worker.position==WorkPosition.WAREHOUSER for worker in instance.workers.all()]
        return all(is_warehouser)
