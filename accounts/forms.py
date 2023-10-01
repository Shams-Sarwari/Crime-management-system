from typing import Any, Dict
from django.contrib.auth.forms import UserCreationForm
from .models import User, DriverProfile, Address, StaffProfile, WorkPlace
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

class CustomDriverUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'licence_num', 'is_active']

    def clean_licence_num(self):
        data = self.cleaned_data['licence_num']
        if User.objects.filter(licence_num=data).exists():
            raise forms.ValidationError('این لایسنس نمبر قبلا وارد سیستم گردیده.')
        return data


class DriverEditForm(forms.ModelForm):
    class Meta: 
        model = DriverProfile
        fields = "__all__"
        exclude = ['user', 'id', 'current_address']

    def clean_licence_num(self):
        data = self.cleaned_data['licence_num']
        if data != self.instance.licence_num:
            qs = User.objects.filter(licence_num = data)
            if qs.exists():
                raise forms.ValidationError('این لایسنس نمبر قبلا وارد سیستم گردیده.')
            return data

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"

class CustomStaffCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_superuser']
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('این ایمیل قبلا در سیستم ثبت شده')
        return data

class StaffEditForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = "__all__"
        exclude = ['user', 'id', 'current_address', 'work_place']
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if data != self.instance.email:
            qs = User.objects.filter(email=data)
            if qs.exists():
                raise forms.ValidationError('این ایمیل قبلا در سیستم ثبت شده')
            return data


class WorkPlaceForm(forms.ModelForm):
    class Meta:
        model = WorkPlace
        fields = "__all__"
    

class CustomPasswordResetForm(forms.Form):
    email_or_licence = forms.CharField(label='ایمیل یا لایسنس نمبر خود را وارد کنید')

    def clean_email_or_licence(self):
        email_or_licence = self.cleaned_data.get('email_or_licence')
        if not email_or_licence:
            raise ValidationError('لطفا ایمیل یا لایسنس نمبر خود را وارد کنید')
        return email_or_licence
    
    def save(self, **kwargs):
        pass