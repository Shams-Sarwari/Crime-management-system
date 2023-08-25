from django.contrib.auth.forms import UserCreationForm
from .models import User, DriverProfile, Address, StaffProfile, WorkPlace
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

class CustomStaffCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_superuser']

class StaffEditForm(ModelForm):
    class Meta:
        model = StaffProfile
        fields = "__all__"
        exclude = ['user', 'id', 'current_address', 'work_place']


class WorkPlaceForm(ModelForm):
    class Meta:
        model = WorkPlace
        fields = "__all__"