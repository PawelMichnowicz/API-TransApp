import uuid
import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models import F, Q
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from transport.models import Transport

from .constants import StatusChoice

from .constants import WEEKDAYS


class ActionChoice(models.TextChoices):
    SEND = 'send', 'Send'
    RECEIVE = 'receive', 'Receive'


class Time(models.Model):

    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=Q(from_hour__lt=F('to_hour')),
                name='%(class)s_check_hours'
            )
        ]


class Warehouse(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}_{self.pk}'


class OpenningTime(Time):

    weekday = models.IntegerField(choices=WEEKDAYS)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name='openning_time')

    def __str__(self):
        return f"{self.get_weekday_display()} {self.from_hour.strftime('%H:%M')}-{self.to_hour.strftime('%H:%M')}"


class ActionWindow(Time):

    monthday = models.DateField()
    action_type = models.CharField(
        max_length=255, choices=ActionChoice.choices)
    warehouse = models.ForeignKey(
        Warehouse, related_name='action_window', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.monthday.strftime('%b%d')} {self.from_hour.strftime('%H:%M')}-{self.to_hour.strftime('%H:%M')}  "


class Action(models.Model):

    action_id = models.UUIDField(default=uuid.uuid4, editable=False)
    action_type = models.CharField(
        max_length=255, choices=ActionChoice.choices)
    date = models.DateTimeField(auto_now_add=True)
    workers = models.ManyToManyField(get_user_model())
    duration = models.DurationField()
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name='actions')
    action_window = models.ForeignKey(
        ActionWindow, on_delete=models.CASCADE, related_name='action')
    transport = models.ForeignKey(
        Transport, on_delete=models.CASCADE, related_name='action')
    status = models.CharField(max_length=25, choices=StatusChoice.choices)

    class Meta:
        unique_together = ('action_id', 'status',)

    def __str__(self):
        return f'{str(self.action_type).casefold()}_{str(self.status)}-{str(self.action_id)}'


