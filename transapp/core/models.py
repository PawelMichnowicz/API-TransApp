from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from storage.models import Warehouse

class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):

        if not username:
            raise ValueError('need to provide username.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):

        user = self.create_user(username, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser, PermissionsMixin):

    USER = 'USR'
    DIRECTOR = 'DIR'
    WAREHOUSER = 'WHR'

    CHOICES = (
        (USER, 'User'),
        (WAREHOUSER, 'Warehouser'),
        (DIRECTOR, 'Director'),
    )

    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    position = models.CharField(max_length=3, choices=CHOICES, default=USER)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='workers', blank=True, null=True, default=None) # workplace - contentype

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'
