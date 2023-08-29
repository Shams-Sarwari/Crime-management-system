from django.db import models
from accounts.models import DriverProfile, StaffProfile

class CarOwner(models.Model):
    GENDER = (
        ("آقا", "آقا"),
        ("خانم", "خانم"),
    )
    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    father_name = models.CharField(max_length=200)
    tazkira_number = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='آقا')
    phone_number = models.CharField(max_length=200, unique=True)
    place_of_work = models.CharField(max_length=200, null=True, blank=True)
    main_address = models.CharField(max_length=200, blank=True, null=True)
    current_address = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='Carowner/image', null=True, blank=True)
    id_image_front = models.ImageField(upload_to='id/image', null=True, blank=True)
    id_image_back = models.ImageField(upload_to='id/image', null=True, blank=True)
    
    

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Car(models.Model):
    STEERING_SIDE = (
        ('راسته', 'راسته'),
        ('چپه', 'چپه')
    )
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True, blank=True)
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
    number_of_rider = models.CharField(
        max_length=255, help_text='تعداد راکبین')
    
    def __str__(self) -> str:
        return f'car with plate: {self.plate_number} and engine num: {self.engine_num}'
    

class JawazSayr(models.Model):
    jawaz_num = models.CharField(max_length=200, primary_key=True, unique=True)
    card_num = models.CharField(max_length=200, unique=True, blank=True, null=True)
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    statistic_num = models.CharField(max_length=200, blank=True, null=True)
    document_num = models.CharField(max_length=200, blank=True, null=True)
    document_date = models.DateTimeField(blank=True, null=True)
    news_num = models.CharField(max_length=200, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    bank_reg_num = models.CharField(max_length=200)
    bank_reg_date = models.DateField()
    size = models.CharField(max_length=200, blank=True, null=True)
    rest_assured = models.CharField(max_length=255, null=True, blank=True, help_text='اطمینانیه مستوفیت')
    verified_by = models.OneToOneField(StaffProfile, on_delete=models.SET_NULL, null=True)
    created = models.DateField()
    expiry_date = models.DateField()

    def __str__(self) -> str:
        return f'Jawaz Sayr of {self.driver.first_name}'
    
