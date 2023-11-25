from django.db import models
from accounts.models import DriverProfile, StaffProfile
from cars.models import Car, CarOwner
# Create your models here.
class Payment(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, null=True, blank=True)
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(CarOwner,on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=0)
    online = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'staff {self.staff} recieved {self.price} on {self.created}'


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
    stuff = models.ForeignKey(StaffProfile, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    crime = models.ForeignKey(Crime, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pending = models.BooleanField(default=False)
    expiry_fine = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    expiry_date = models.DateField()
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'plate: {self.car.plate_number} price: {self.price}'

    def get_total(self):
        return self.price + self.expiry_fine
    


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField()
    read = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

