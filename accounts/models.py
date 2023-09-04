from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password
import uuid
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

class StaffProfile(models.Model):
    GENDER = (
        ('آقا', 'آقا'),
        ('خانم', 'خانم'), 
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=300, unique=True, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    father_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=5, choices=GENDER, default='آقا')
    tazkira_num = models.CharField(max_length=255)
    current_address = models.OneToOneField('Address', on_delete=models.CASCADE, null=True)
    work_place = models.ForeignKey('WorkPlace', on_delete=models.SET_NULL, null=True)
    phone_num = models.CharField(max_length=14,unique=True, null=True, blank=True)
    tazkira_img = models.ImageField(upload_to="media/staff/id_images")
    avatar = models.ImageField(upload_to="media/staff/profile_images", default="media/staff.jpg", null=True, blank=True)
   

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def set_password(self, raw_password):
        if len(raw_password) < 8:
            raise ValueError('پسورد باید حداقل دارای هشت کارکتر باشد')
        else: 
            self.password = make_password(raw_password)

class WorkPlace(models.Model):
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.district}, {self.province}'



class DriverProfile(models.Model):
    GENDER = (
        ('آقا', 'آقا'),
        ('خانم', 'خانم'), 
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    licence_num = models.CharField(max_length=250, unique=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    father_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=5, choices=GENDER, default='آقا')
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    tazkira_num = models.CharField(max_length=255)
    current_address = models.OneToOneField('Address', on_delete=models.CASCADE, blank=True, null=True)
    phone_num = models.CharField(max_length=14,unique=True, null=True, blank=True)
    tazkira_img = models.ImageField(upload_to="media/driver/id_images", default="media/driver_id.jpg", null=True, blank=True)
    avatar = models.ImageField(upload_to="media/driver/profile_images", default="media/driver.jpg", null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self) -> str:
        return f'{self.first_name}, {self.last_name}, {self.licence_num}'


class Address(models.Model):
    province = models.CharField(max_length=100,blank=True, null=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100,null=True, blank=True)
    house_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.province}, {self.district}, {self.street}, {self.house_number}'