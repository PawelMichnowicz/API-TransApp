import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime

from .constants import DEFAULT_TIME_OPEN, WEEKDAYS, TimespanActionEnum


class Time(models.Model):

    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        abstract = True


class OpenningTime(Time):

    weekday = models.IntegerField(
        choices=WEEKDAYS)

    def __str__(self):
        return f"{self.get_weekday_display()} {self.from_hour.strftime('%H:%M')}-{self.to_hour.strftime('%H:%M')}"


class Timespan(Time):

    class TimespanAction(models.TextChoices):
        SEND = TimespanActionEnum.SEND.name.lower(), 'Send'
        RECEIVE = TimespanActionEnum.RECEIVE.name.lower(), 'Receive'

    monthday = models.DateField()
    action = models.CharField(max_length=255, choices=TimespanAction.choices)

    def __str__(self):
        action = f"{self.action}".upper()
        return f"{action} {self.monthday.strftime('%b%d')} {self.from_hour.strftime('%H:%M')}-{self.to_hour.strftime('%H:%M')}"


class Warehouse(models.Model):

    name = models.CharField(max_length=255, unique=True)
    openning_time = models.ManyToManyField(OpenningTime)
    action_available = models.ManyToManyField(
        Timespan, related_name='warehouse_action', blank=True)
    description = models.TextField(default='')
    # workers

    def __str__(self):
        return self.name

@receiver(post_save, sender=Warehouse, dispatch_uid='set_department')
def set_default_open_time(**kwargs):

    warehouse = kwargs['instance']

    if not warehouse.openning_time.all():
        for day, hour in enumerate(DEFAULT_TIME_OPEN, 1):
            day_model = OpenningTime.objects.get_or_create(weekday=day, from_hour=datetime.time(
                hour[0], 0), to_hour=datetime.time(hour[1], 0))[0]
            warehouse.openning_time.add(day_model)
        warehouse.save()


class Action(models.Model):

    workers = models.ManyToManyField(get_user_model())
    duration = models.DurationField(
        default=datetime.timedelta(seconds=(60*60)))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    id_offer = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField(default='')
    action_type = models.CharField(max_length=255, default=TimespanActionEnum.SEND)

