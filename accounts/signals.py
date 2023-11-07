from .models import DriverProfile, User, StaffProfile
from cars.models import CarOwner
from django.db.models.signals import post_delete, post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
import uuid

@receiver(post_save, sender=get_user_model())
def create_driver_or_staff_profile(sender, instance, created, **kwargs):
    if created and instance.is_driver:  
        driver = DriverProfile.objects.create(
            user = instance,
            licence_num = instance.username, 
            
        )
    elif created and instance.is_owner:
        owner = CarOwner.objects.create(
            user=instance,
            tazkira_number = instance.username,
        )
    elif created and instance.is_staff:
        staff = StaffProfile.objects.create(
            user = instance,
            email = instance.email,
            
        )

@receiver(post_save, sender=DriverProfile)
def update_driver_user(sender, instance, created, **kwargs):
    user = instance.user
    if user.username != instance.licence_num:
        user.username = instance.licence_num
        user.save()

@receiver(post_save, sender=StaffProfile)
def update_staff_user(sender, instance, created, **kwargs):
    user = instance.user
    if user.email != instance.email:
        user.email = instance.email
        user.save()
        
def delete_driver_or_staff_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()




post_delete.connect(delete_driver_or_staff_user, sender=DriverProfile)
post_delete.connect(delete_driver_or_staff_user, sender=StaffProfile)
