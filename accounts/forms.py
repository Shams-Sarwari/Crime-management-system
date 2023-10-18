from typing import Any, Dict
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm
from .models import User, DriverProfile, Address, StaffProfile, WorkPlace
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

class CustomDriverUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'licence_num', 'is_active', 'password1', 'password2']
        
        
    def __init__(self, *args, **kwargs):
        super(CustomDriverUserCreationForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            if k != 'is_active':
                v.widget.attrs.update(
                    {'class':'driver-form-input'}
                )
            else: 
                v.widget.attrs.update(
                    {'id': 'myCheckbox', 'checked': 'checked'}
                )

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
    
    def __init__(self, *args, **kwargs):
        super(DriverEditForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            if k=='gender':
                v.widget.attrs.update(
                    {'class':'h-7 w-28 bg-color-primary text-white text-xs text-center rounded  outline-none'}
            )
            elif k=='tazkira_img' or k=='avatar':
                v.widget.attrs.update(
                    {'class':'input-file'}
            )
            else:
                v.widget.attrs.update(
                    {'class':'driver-form-input'}
            )
            


    # def clean_licence_num(self):
    #     data = self.cleaned_data['licence_num']
    #     if data != self.instance.licence_num:
    #         qs = User.objects.filter(licence_num = data)
    #         if qs.exists():
    #             raise forms.ValidationError('این لایسنس نمبر قبلا وارد سیستم گردیده.')
    #         return data

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            v.widget.attrs.update(
                    {'class':'driver-form-input'}
            )
    
class CustomStaffCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super(CustomStaffCreationForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            if k == 'is_active':
                v.widget.attrs.update(
                    {'id': 'myCheckbox', 'checked': 'checked'}
                    
                )
            elif k == 'is_superuser':
                v.widget.attrs.update(
                    {'id': 'myCheckbox'}
                )
            else: 
                v.widget.attrs.update(
                    {'class':'driver-form-input'}
                )

    
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
    
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            if k == 'gender':
                v.widget.attrs.update(
                    {'class': 'h-7 w-28 bg-color-primary text-white text-xs text-center rounded  outline-none'}
                )
            elif k=='tazkira_img':
                v.widget.attrs.update(
                    {'class': 'input-file'}
                )
            else: 
                v.widget.attrs.update(
                        {'class':'driver-form-input'}
                )

    
    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if data != self.instance.email:
    #         qs = User.objects.filter(email=data)
    #         if qs.exists():
    #             raise forms.ValidationError('این ایمیل قبلا در سیستم ثبت شده')
    #         return data


class WorkPlaceForm(forms.ModelForm):
    class Meta:
        model = WorkPlace
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(WorkPlaceForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            v.widget.attrs.update(
                    {'class':'driver-form-input'}
            )
    

class CustomPasswordResetForm(forms.Form):
    email_or_licence = forms.CharField(label='ایمیل یا لایسنس نمبر خود را وارد کنید')

    def clean_email_or_licence(self):
        email_or_licence = self.cleaned_data.get('email_or_licence')
        if not email_or_licence:
            raise ValidationError('لطفا ایمیل یا لایسنس نمبر خود را وارد کنید')
        return email_or_licence
    
    def save(self, **kwargs):
        pass


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        
        
        for k, v in self.fields.items():
            if k == 'old_password':
                v.widget.attrs.update(
                        {'class':'driver-form-input tracking-widest', 
                        'id': 'current-pass-input'}
                )
            elif k == 'new_password1': 
                v.widget.attrs.update(
                        {'class':'driver-form-input tracking-widest', 
                        'id': 'new-pass-input'}
                )
            elif k == 'new_password2':
                v.widget.attrs.update(
                        {'class':'driver-form-input tracking-widest', 
                        'id': 'confirm-pass-input'}
                )