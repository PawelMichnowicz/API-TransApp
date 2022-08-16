from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from storage.models import Warehouse


class WorkPosition(models.TextChoices):
    USER = 'USR', 'User'
    WAREHOUSER = 'WHR', 'Warehouser'
    DIRECTOR = 'DIR', 'Director'
    ADMIN = 'ADM', 'Admin'
    COORDINATOR = 'COR', 'Coordinator'


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('need to provide email.')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser, PermissionsMixin):


    email = models.EmailField(max_length=255, blank=True, null=True, default=None, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    position = models.CharField(max_length=255, choices=WorkPosition.choices, default=WorkPosition.USER)
    workplace = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, related_name='workers', blank=True, null=True, default=None)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

