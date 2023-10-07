from django.db import models
from accounts.models import DriverProfile, StaffProfile
from cars.models import Car
# Create your models here.
class Crime(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.min_price}-{self.max_price} {self.title}'
    
class CarCrime(models.Model):
    stuff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'plate: {self.car.plate_number} price: {self.price} {self.crime.title[:50]}'