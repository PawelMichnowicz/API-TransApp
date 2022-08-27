'''
Models for storage APIs
'''
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q
from django.core.exceptions import ValidationError

from transport.models import Transport

from .constants import WEEKDAYS, StatusChoice


class ActionChoice(models.TextChoices):
    ''' Choices for type of action '''
    SEND = 'send', 'Send'
    RECEIVE = 'receive', 'Receive'


class Time(models.Model):
    ''' Base model for models using time '''
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        ''' Set model as abstract and check if hours are correct '''
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=Q(from_hour__lt=F('to_hour')),
                name='%(class)s_check_hours'),
            ]


class Warehouse(models.Model):
    ''' Warehouse model '''
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}_{self.pk}'


class OpenningTime(Time):
    ''' Openning hours model '''
    weekday = models.IntegerField(choices=WEEKDAYS)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name='openning_time')

    def __str__(self):
        return f"{self.get_weekday_display()} {self.from_hour.strftime('%H:%M')}-{self.to_hour.strftime('%H:%M')}"


class ActionWindow(Time):
    ''' Action window model which represent possible time for warehouse action '''
    monthday = models.DateField()
    action_type = models.CharField(
        max_length=255, choices=ActionChoice.choices)
    warehouse = models.ForeignKey(
        Warehouse, related_name='action_window', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.monthday.strftime('%b%d')} {self.from_hour.strftime('%H:%M')}-{self.to_hour.strftime('%H:%M')}"


class Action(models.Model):
    ''' Action model which represent receive or send deliver from warehouse '''
    action_id = models.UUIDField(default=uuid.uuid4, editable=False)
    action_type = models.CharField(
        max_length=255, choices=ActionChoice.choices)
    date = models.DateTimeField(auto_now_add=True)
    workers = models.ManyToManyField(get_user_model(), blank=True)
    duration = models.DurationField(null=True, blank=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name='actions', null=True, blank=True)
    action_window = models.ForeignKey(
        ActionWindow, on_delete=models.CASCADE, related_name='action', null=True, blank=True)
    transport = models.ForeignKey(
        Transport, on_delete=models.CASCADE, related_name='action')
    status = models.CharField(max_length=25, choices=StatusChoice.choices)


    class Meta:
        ''' check if each action has the appropriate fields included '''
        unique_together = ('action_id', 'status',)
        constraints = [
            models.CheckConstraint(
                check=(Q(status=StatusChoice.DELIVERED, duration__isnull=False)) |
                      (Q(status=StatusChoice.DELIVERED_BROKEN, duration__isnull=False)) |
                      (Q(status=StatusChoice.IN_PROGRESS, duration__isnull=True)) |
                      (Q(status=StatusChoice.UNREADY, duration__isnull=True, warehouse__isnull=True)) ,
                name='check_status_correct'
                )
            ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if (self.status==StatusChoice.UNREADY or self.status==StatusChoice.IN_PROGRESS) and self.workers.exists():
            raise ValidationError('This action cannot contain workers')
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{str(self.action_type).casefold()}_{str(self.status)}-{str(self.action_id)}'


