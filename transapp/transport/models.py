from django.db import models
import uuid

# Create your models here.

class Vehicle(models.Model):

    registration = models.CharField(max_length=30, unique=True)
    capacity = models.IntegerField()
    is_refrigerate = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    description = models.TextField(default='')

    class Meta:
        ordering = ['is_available', '-capacity']

    def __str__(self):
        return self.registration + "___" + str(self.capacity) + "l"


class Route(models.Model):

    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    duration = models.DurationField(blank=True, null=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.origin + "->" + self.destination


class Offer(models.Model):

    id_offer = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='offers')
    need_refrigerate = models.BooleanField(default=False)
    description = models.TextField(default='')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True, default=None)
    accepted = models.BooleanField(default=False)






