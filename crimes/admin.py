from django.contrib import admin
from .models import Crime, CarCrime, Payment
# Register your models here.


admin.site.register(Crime)
admin.site.register(CarCrime)
admin.site.register(Payment)
