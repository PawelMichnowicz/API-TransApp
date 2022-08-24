from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Vehicle(models.Model):

    registration = models.CharField(max_length=30, unique=True)
    capacity = models.IntegerField()
    is_refrigerate = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['is_available', '-capacity']

    def __str__(self):
        return self.registration + "___" + str(self.capacity)


class Route(models.Model):

    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    duration = models.DurationField(blank=True, null=True)

    def __str__(self):
        return self.origin + "->" + self.destination


class Transport(models.Model):

    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    need_refrigerate = models.BooleanField(default=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True, default=None)


class Order(models.Model):

    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    buyer_email = models.EmailField()
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='orders')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    products = ArrayField(models.IntegerField())
    broken = models.BooleanField(default=False)


    def __str__(self):
        return str(self.order_id)






