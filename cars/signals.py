# from .models import Car, CarHistory
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# @receiver(post_save, sender=Car)
# def create_car_history(sender, instance, created, **kwargs):
#     if not created:
#         original_car = Car.objects.get(id=instance.id)
#         if instance.driver != original_car.driver:
#             history = CarHistory.objects.create(
#                 car = instance, 
#                 driver = instance.driver,

#             )
#             history.save()

        