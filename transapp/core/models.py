from asyncio import FastChildWatcher
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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


class User(AbstractBaseUser):

    CHOICES = (
        ('USR', 'User'),
        ('DIR', 'Director'),
    )

    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    position = models.CharField(max_length=3, choices=CHOICES, default=CHOICES[0])

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'position']
