'''
Models for document APIs
'''
from django.db import models

class Document(models.Model):
    ''' Document model '''
    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='documents')