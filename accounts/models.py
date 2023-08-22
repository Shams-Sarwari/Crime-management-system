from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
# Create your models here.
class UserAccountManager(BaseUserManager):
    def create_user(self, username, email, password, licence_num=None):
        
        if not email:
            raise ValueError('User must have email')
        if not username:
            raise ValueError('User must have username')

        email = self.normalize_email(email)
        user = self.model(username = username, email = email)
        user.set_password(password)
        user.is_staff = True
        user.save()
        return user

    

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=300)
    email = models.EmailField(max_length=300, unique=True, blank=True, null=True)
    licence_num = models.CharField(max_length=100, unique=True, blank=True, null=True)

    is_driver = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    joined_date = models.DateTimeField(default=timezone.now)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
