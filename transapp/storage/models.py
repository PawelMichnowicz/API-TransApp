from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime

DEFAULT_TIME_OPEN = [(8,16), (8,16), (8,16), (8,16), (8,16)]

WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]

TIMESPAN_ACTIONS = ['send', 'receive']

class Time(models.Model):

    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        abstract = True


class OpenningTime(Time):

    weekday = models.IntegerField(
        choices=WEEKDAYS)

    def __str__(self) :
        return f"{self.get_weekday_display()} {self.from_hour}-{self.to_hour}"


class Timespan(Time):

    monthday = models.DateField()

    def __str__(self) :
        return f"{self.monthday} {self.from_hour}-{self.to_hour}"

class Timedelta(Time):
    # not use
    def save(self, *args, **kwargs):
        self.duration = self.from_hour - self.to_hour
        super(Timedelta, self).save(*args, **kwargs)

################################################################################

class Warehouse(models.Model):

    name = models.CharField(max_length=255, unique=True)
    openning_time = models.ManyToManyField(OpenningTime)
    receive_available = models.ManyToManyField(Timespan, related_name='warehouse_receive', blank=True)
    send_available = models.ManyToManyField(Timespan, related_name='warehouse_send', blank=True)
    description = models.TextField(default='')
    # workers

    def __str__(self):
        return self.name

@receiver(post_save, sender=Warehouse, dispatch_uid='set_department')
def set_default_open_time(**kwargs):

    warehouse = kwargs['instance']

    if not warehouse.openning_time.all():
        for day, hour in enumerate(DEFAULT_TIME_OPEN, 1):
            day_model = OpenningTime.objects.get_or_create(weekday=day, from_hour=datetime.time(hour[0], 0), to_hour=datetime.time(hour[1], 0))[0]
            warehouse.openning_time.add(day_model)
        warehouse.save()



class ReceiveAction(models.Model):

    workers = models.ManyToManyField(get_user_model())
    duration = models.DurationField(default=datetime.timedelta(seconds=(60*60)))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    id_offer = models.CharField(max_length=5)
    description = models.TextField(default='')


class SendAction(models.Model):

    workers = models.ManyToManyField(get_user_model())
    duration = models.DurationField(default=datetime.timedelta(seconds=(60*60)))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    id_offer = models.CharField(max_length=5)
    description = models.TextField(default='')




