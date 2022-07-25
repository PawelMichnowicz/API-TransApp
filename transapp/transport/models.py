from django.db import models
from django.utils.crypto import get_random_string

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

    id_offer = models.CharField(max_length=5)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='offers')
    need_refrigerate = models.BooleanField(default=False)
    description = models.TextField(default='')

    def save(self, *args, **kwargs):
        if not self.id_offer:
            while True:
                id_offer = get_random_string(length=5)
                if not Offer.objects.filter(id_offer=id_offer).exists() and not AcceptedOffer.objects.filter(id_offer=id_offer).exists():
                    break
            self.id_offer = id_offer
        return super().save(*args, **kwargs)

    def accept(self, vehicle: Vehicle):
        if not vehicle.is_available:
            raise Exception('Vehicle is unavailable')
        elif self.need_refrigerate and not vehicle.is_refrigerate:
            raise Exception('Vehicle need refigerator')

        AcceptedOffer(id_offer=self.id_offer, vehicle=vehicle, route=self.route, description=self.description).save()
        self.delete()
        vehicle.is_available = False
        vehicle.save()


class AcceptedOffer(models.Model):

    id_offer = models.CharField(max_length=5)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    description = models.TextField(default='')



