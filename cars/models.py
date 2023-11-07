from django.db import models
from accounts.models import DriverProfile, StaffProfile, User
import uuid

class CarOwner(models.Model):
    GENDER = (
        ("آقا", "آقا"),
        ("خانم", "خانم"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    father_name = models.CharField(max_length=200)
    tazkira_number = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='آقا')
    phone_number = models.CharField(max_length=200)
    place_of_work = models.CharField(max_length=200, null=True, blank=True)
    main_address = models.CharField(max_length=200, blank=True, null=True)
    current_address = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='Carowner/image', default="owner.jpg")
    id_image_front = models.ImageField(upload_to='id/image', null=True, blank=True)
    id_image_back = models.ImageField(upload_to='id/image', null=True, blank=True)
    
    

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Car(models.Model):
    STEERING_SIDE = (
        ('راسته', 'راسته'),
        ('چپه', 'چپه')
    )
    owner = models.ForeignKey('CarOwner', on_delete=models.SET_NULL, null=True, blank=True)
    plate_number = models.CharField(max_length=200, blank=True, null=True)
    steering = models.CharField(max_length=10, choices=STEERING_SIDE, default='راسته')
    model = models.CharField(max_length=300)
    color = models.CharField(max_length=200)
    engine_type = models.CharField(max_length=300)
    engine_num = models.CharField(max_length=200)
    number_of_cylinder = models.IntegerField()
    chassis_num = models.CharField(max_length=200, help_text='شماره شاسی')
    legal_weight = models.CharField(
        max_length=255, null=True, blank=True, help_text='وزن مجموعی مجاز')
    weight_on_axle = models.CharField(
        max_length=255, null=True, blank=True, help_text='وزن بالای اکسل')
    number_of_rider = models.PositiveIntegerField(help_text='تعداد راکبین')
    
    def __str__(self) -> str:    
        return f'car with plate: {self.plate_number} and engine num: {self.engine_num}'
    
    
    

class JawazSayr(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    jawaz_num = models.CharField(max_length=200, primary_key=False, unique=True)
    card_num = models.CharField(max_length=200, unique=True, blank=True, null=True)
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    statistic_num = models.CharField(max_length=200, blank=True, null=True)
    document_num = models.CharField(max_length=200, blank=True, null=True)
    document_date = models.DateField(null=True)
    news_num = models.CharField(max_length=200, blank=True, null=True)
    news_date = models.DateField( null=True)
    bank_reg_num = models.CharField(max_length=200)
    bank_reg_date = models.DateField()
    size = models.CharField(max_length=200, blank=True, null=True)
    rest_assured = models.CharField(max_length=255, null=True, blank=True, help_text='اطمینانیه مستوفیت')
    verified_by = models.ForeignKey(StaffProfile, on_delete=models.SET_NULL, null=True)
    created = models.DateField()
    expiry_date = models.DateField()

    def __str__(self) -> str:
        return self.jawaz_num
    


class CarHistory(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'History for car with plate: {self.car.plate_number} engine number: {self.car.engine_num}'


class OldHistory(models.Model):
    car_history = models.OneToOneField(CarHistory, on_delete=models.CASCADE)
    old_driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True, blank=True)
    old_owner = models.ForeignKey(CarOwner, on_delete=models.SET_NULL, null=True, blank=True)
    
    