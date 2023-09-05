from django.contrib import admin
from .models import Car, CarOwner, JawazSayr, CarHistory
# Register your models here.


admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(JawazSayr)
admin.site.register(CarHistory)