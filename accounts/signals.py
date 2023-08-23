from .models import DriverProfile, User, StaffProfile
from django.db.models.signals import post_delete, post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
import uuid

@receiver(post_save, sender=get_user_model())
def create_driver_or_staff_profile(sender, instance, created, **kwargs):
    if created and instance.is_driver:  
        driver = DriverProfile.objects.create(
            user = instance,
            first_name = instance.username,
            licence_num = instance.licence_num, 
            
        )
    elif created and instance.is_staff:
        staff = StaffProfile.objects.create(
            user = instance,
            first_name = instance.username,
            email = instance.email,
            
        )

        
def delete_driver_or_staff_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()



post_save.connect(create_driver_or_staff_profile, sender=get_user_model())
post_delete.connect(delete_driver_or_staff_user, sender=DriverProfile)
