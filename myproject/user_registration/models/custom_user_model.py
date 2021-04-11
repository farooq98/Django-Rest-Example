from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from core import generate_random_code, send_verfication_email

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
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class UserModel(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100, default='Anonymous')
    username = models.CharField(max_length=20, unique=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    email_verification_time = models.DateTimeField(null=True, blank=True)
    password_change_time = models.DateTimeField(null=True, blank=True)
    #password field is already defined in AbstractBaseUser

    objects = MyCustomUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def change_password(self):
        if self.is_active:
            self.verification_code = generate_random_code()
            send_verfication_email(self.email, self.verification_code, purpose="password reset")
            self.password_change_time = timezone.now() + timedelta(minutes=10)
            self.save()

    def send_email(self):
        if not self.is_active:
            self.verification_code = generate_random_code()
            send_verfication_email(self.email, self.verification_code)
            self.email_verification_time = timezone.now() + timedelta(minutes=10)

    def verify_email_code(self, code):
        if code == self.verification_code and timezone.now() < self.email_verification_time:
            return True
        else:
            return False
    
    def verify_change_pass_code(self, code):
        if code == self.verification_code and timezone.now() < self.password_change_time:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)