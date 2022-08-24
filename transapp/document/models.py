from django.db import models

class Document(models.Model):

    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='documents')