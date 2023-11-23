from typing import Any, Dict
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm
from .models import User, DriverProfile, Address, StaffProfile, WorkPlace
from cars.models import CarOwner
from django import forms
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.core.exceptions import ValidationError

class CustomDriverUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','is_active', 'password1', 'password2']
        
        
    def __init__(self, *args, **kwargs):
        super(CustomDriverUserCreationForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            if k != 'is_active':
                v.widget.attrs.update(
                    {'class':'myinput'}
                )
            else: 
                v.widget.attrs.update(
                    {'id': 'myCheckbox', 'checked': 'checked'}
                )

    
class DriverEditForm(forms.ModelForm):
    class Meta: 
        model = DriverProfile
        fields = "__all__"
        exclude = ['user', 'id', 'current_address', 'licence_num', 'avatar', 'tazkira_img']
    
    def __init__(self, *args, **kwargs):
        super(DriverEditForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            if k=='gender':
                v.widget.attrs.update(
                    {'class':'text-center myinput'}
            )
            elif k=='avatar':
                v.widget.attrs.update(
                    {'class':'hidden',
                     'type': 'file',
                     'id': 'profilePhoto',
                     'alt': '',
                     'onchange': 'updateProfileFileName(this);'}
            )
            elif k=='tazkira_img':
                v.widget.attrs.update(
                    {'class':'hidden',
                     'type': 'file',
                     'id': 'tazkiraPhoto',
                     'onchange': 'updateTazkiraFileName(this);'}
            )
            else:
                v.widget.attrs.update(
                    {'class':'myinput'}
            )
            

class OwnerEditForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = '__all__'
        exclude = ['user']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            v.widget.attrs.update(
                    {'class':'myinput'}
            )
    
class CustomStaffCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','is_active', 'is_superuser']
        exclude = ['username']

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
                    {'class':'myinput'}
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
        exclude = ['user', 'id', 'current_address', 'work_place', 'tazkira_img', 'avatar', 'email']
    
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            if k == 'gender':
                v.widget.attrs.update(
                    {'class': 'myinput text-center'}
                )
            elif k=='tazkira_img':
                v.widget.attrs.update(
                    {'class': 'input-file'}
                )
            else: 
                v.widget.attrs.update(
                        {'class':'myinput'}
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
                    {'class':'myinput'}
            )
    

class CustomPasswordResetForm(forms.Form):
    email_or_licence = forms.CharField(label='ایمیل یا لایسنس نمبر خود را وارد کنید')

    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        
        
        for k, v in self.fields.items():
            
            v.widget.attrs.update(
                {'class':'w-full h-7 mb-5 px-4 bg-gray-50 rounded outline-none placeholder:text-xs placeholder:text-gray-400',
                'placeholder':"ورودی",
                }
            )
    

    def clean_email_or_licence(self):
        email_or_licence = self.cleaned_data.get('email_or_licence')
        if not email_or_licence:
            raise ValidationError('ایمیل یا لایسنس وارد شده در سیستم موجود نمی باشد')
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

class CustomSetPasswordForm(SetPasswordForm):
    
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            
            v.widget.attrs.update(
                {'class':'bg-gray-50 border border-gray-300  outline-none text-gray-900 sm:text-sm tracking-widest rounded-lg focus:border-gray-400 focus:ring-primary-600  block w-full p-2.5',
                'placeholder':"••••••••",
                }
            )