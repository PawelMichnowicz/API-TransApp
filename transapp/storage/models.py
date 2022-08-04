import uuid
import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models import F, Q
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


from .constants import DEFAULT_TIME_OPEN, WEEKDAYS

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
    action = models.CharField(max_length=255, choices=ActionChoice.choices)

    def __str__(self):
        action = f"{self.action}".upper()
        return f"{action} {self.monthday.strftime('%b%d')} {self.from_hour.strftime('%H:%M')}-{self.to_hour.strftime('%H:%M')}"


class OpenningTime(Time):

    weekday = models.IntegerField(
        choices=WEEKDAYS)

    def __str__(self):
        return f"{self.get_weekday_display()} {self.from_hour.strftime('%H:%M')}-{self.to_hour.strftime('%H:%M')}"


class Warehouse(models.Model):

    name = models.CharField(max_length=255, unique=True)
    openning_time = models.ManyToManyField(OpenningTime)
    action_available = models.ManyToManyField(
        Timespan, related_name='warehouse_action', blank=True)

    def __str__(self):
        return self.name



class Action(models.Model):

    workers = models.ManyToManyField(get_user_model())
    duration = models.DurationField(
        default=datetime.timedelta(seconds=(60*60)))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    id_offer = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    action_type = models.CharField(max_length=255, choices=ActionChoice.choices)

