from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from core import generate_random_code, send_verification_email
from django.conf import settings

class MyCustomUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.send_email()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=20, unique=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    verification_code_timeout = models.DateTimeField(null=True, blank=True)
    is_workspace_admin = models.BooleanField(default=False)
    designation = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.CharField(max_length=500,null=True,blank=True)
    #password field is already defined in AbstractBaseUser

    objects = MyCustomUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def change_password(self):
        if self.is_active:
            self.verification_code = generate_random_code()
            if not settings.DEBUG:
                send_verification_email(self.email, self.verification_code, purpose="password reset", link=f"HappySpace://forgot/{self.email}/{self.verification_code}/")
            self.verification_code_timeout = timezone.now() + timedelta(minutes=10)
            self.save()

    def send_email(self):
        if not self.is_active:
            self.verification_code = generate_random_code()
            if not settings.DEBUG:
                send_verification_email(self.email, self.verification_code)
            self.verification_code_timeout = timezone.now() + timedelta(minutes=10)
            self.save()

    def validate_timeout(self, code):
        if code == self.verification_code and timezone.now() < self.verification_code_timeout:
            self.verification_code_timeout = timezone.now()
            self.save()
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)