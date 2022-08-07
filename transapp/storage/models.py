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
    SEND = 'send' , 'Send'
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


class Timespan(Time):

    monthday = models.DateField()
    action_type = models.CharField(max_length=255, choices=ActionChoice.choices)

    def __str__(self):
        return f"{self.monthday.strftime('%b%d')} {self.from_hour.strftime('%H:%M')}-{self.to_hour.strftime('%H:%M')}"


class OpenningTime(Time):

    weekday = models.IntegerField(
        choices=WEEKDAYS)

    def __str__(self):
        return f"{self.get_weekday_display()} {self.from_hour.strftime('%H:%M')}-{self.to_hour.strftime('%H:%M')}"


class Warehouse(models.Model):

    name = models.CharField(max_length=255, unique=True)
    openning_time = models.ManyToManyField(OpenningTime)
    timespan_available = models.ManyToManyField(
        Timespan, related_name='warehouse_action', blank=True)

    def __str__(self):
        return self.name

class Action(models.Model):

    workers = models.ManyToManyField(get_user_model())
    duration = models.DurationField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255, choices=ActionChoice.choices)
    timespan = models.OneToOneField(Timespan, on_delete=models.CASCADE, related_name='action')
    transport = models.OneToOneField(Transport, on_delete=models.CASCADE, related_name='action')
    status = models.CharField(max_length=25, choices=StatusChoice.choices)

    def __str__(self):
        return f'{str(self.transport)}  {str(self.action_type)}  {str(self.status)}'



