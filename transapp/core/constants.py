from django.db import models

class WorkPosition(models.TextChoices):
    '''Choices for user work positions'''
    WAREHOUSER = 'WHR', 'Warehouser'
    DIRECTOR = 'DIR', 'Director'
    ADMIN = 'ADM', 'Admin'
    COORDINATOR = 'COR', 'Coordinator'

