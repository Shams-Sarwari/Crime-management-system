from django.contrib.auth.forms import UserCreationForm
from .models import User, DriverProfile, Address
from django.forms import ModelForm

class CustomDriverUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'licence_num', 'is_active']

class DriverEditForm(ModelForm):
    class Meta: 
        model = DriverProfile
        fields = "__all__"
        exclude = ['user', 'id', 'current_address']

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = "__all__"