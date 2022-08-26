'''
Models for core APIs
'''
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from .constants import WorkPosition
from storage.models import Warehouse


class UserManager(BaseUserManager):
    ''' Manager for user model '''
    def create_user(self, email, password=None, **extra_fields):
        ''' create save and return new user '''
        if not email:
            raise ValueError('need to provide email.')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        ''' create save and return new superuser '''
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser, PermissionsMixin):
    ''' User model in system '''
    email = models.EmailField(max_length=255, blank=True, null=True, default=None, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    position = models.CharField(max_length=255, choices=WorkPosition.choices, default=WorkPosition.WAREHOUSER)
    workplace = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, related_name='workers', blank=True, null=True, default=None)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

