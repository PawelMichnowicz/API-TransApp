'''
Models for document APIs
'''
from django.db import models

class Document(models.Model):
    ''' Document model '''
    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='documents')


class Contractor(models.Model):

    regon = models.CharField(max_length=14)
    nip = models.CharField(max_length=14)
    status_nip = models.CharField(max_length=50, null=True, blank=True)
    nazwa = models.CharField(max_length=100)
    province = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(max_length=30, null=True, blank=True)
    commune = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    street = models.CharField(max_length=30, null=True, blank=True)
    street_number = models.CharField(max_length=15, null=True, blank=True)
    apartment_number = models.CharField(max_length=15, null=True, blank=True)
    type = models.CharField(max_length=10, null=True, blank=True)
    silos_id = models.CharField(max_length=10, null=True, blank=True)
    end_date_activity = models.DateField(null=True, blank=True)
    city_post = models.CharField(max_length=20, null=True, blank=True)

 