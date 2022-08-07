from django.db import models

DEFAULT_TIME_OPEN = [(8, 16), (8, 16), (8, 16), (8, 16), (8, 16)]
WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),]

class StatusChoice(models.TextChoices):
    DELIVERED_BROKEN = 'delivered_broken', 'Delivered with broken products'
    DELIVERED = 'delivered' , 'Delivered with no problems'
    IN_PROGRESS = 'in_progress', 'In progress'
    UNREADY = 'unready', 'Not ready to action'

