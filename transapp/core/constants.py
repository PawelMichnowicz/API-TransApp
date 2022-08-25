from django.db import models

class WorkPosition(models.TextChoices):
    USER = 'USR', 'User'
    WAREHOUSER = 'WHR', 'Warehouser'
    DIRECTOR = 'DIR', 'Director'
    ADMIN = 'ADM', 'Admin'
    COORDINATOR = 'COR', 'Coordinator'
