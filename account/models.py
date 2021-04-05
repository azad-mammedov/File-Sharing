from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone



class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('username must be set')
        # username = self.normalize_username(username)
        user = CustomUser(username = username, is_staff=is_staff,
                    is_superuser=is_superuser, date_joined=now,
                    **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, **extra_fields):
        return self._create_user(username, password, False, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True, **extra_fields)
    









class CustomUser(AbstractUser):
    username = models.CharField('username',max_length=150,unique=True)
    os = models.CharField(max_length=100,blank=True,null=True)
    ip = models.CharField(max_length=20,blank=True,null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username