from django import forms 
from .models import Car, CarOwner, JawazSayr
from accounts.models import DriverProfile


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        exclude = ['driver', 'owner',]
    
    def __init__(self, *args, **kwargs):
        super(CreateCarForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            if k=='steering':
                v.widget.attrs.update(
                    {'class':'h-7 w-28 bg-color-primary text-white text-center rounded  outline-none'}
            )
            
            else:
                v.widget.attrs.update(
                    {'class':'driver-form-input'}
            )
            

    
class EditCarForm(forms.ModelForm):
    driver_licence = forms.CharField(required=False)
    owner_tazkira = forms.CharField(required=False)
    
    class Meta:
        model = Car
        fields = ['driver_licence', 'owner_tazkira', 'plate_number']
        
    
    def clean_driver_licence(self):
        driver_licence = self.cleaned_data['driver_licence']
        if driver_licence:
            try:
                driver = DriverProfile.objects.get(licence_num = driver_licence)
            except DriverProfile.DoesNotExist:
                raise forms.ValidationError("Invalid Driver Licence.")
            return driver
    
    def clean_owner_tazkira(self):
        owner_tazkira = self.cleaned_data['owner_tazkira']
        if owner_tazkira:
            try:
                owner = CarOwner.objects.get(tazkira_number=owner_tazkira)
            except CarOwner.DoesNotExist:
                raise forms.ValidationError('Invalide Tazkira Number for Owner')
            return owner
        
    def save(self, commit=True):
        car = super().save(commit=False)
        driver_licence = self.cleaned_data['driver_licence']
        owner_tazkira = self.cleaned_data['owner_tazkira']
        if driver_licence:
            car.driver = driver_licence
        if owner_tazkira:
            car.owner = owner_tazkira
        if commit:
            car.save()
        return car
    
class CreateOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CreateOwnerForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            if k=='gender':
                v.widget.attrs.update(
                    {'class':'h-7 w-28 bg-color-primary text-white text-center rounded  outline-none'}
            )
            elif k=='id_image_front':
                v.widget.attrs.update(
                    {'class': 'input-file'}
                )
            elif k=='image':
                v.widget.attrs.update(
                    {'class': 'input-file'}
                )
            else:
                v.widget.attrs.update(
                    {'class':'driver-form-input'}
            )

class JawazForm(forms.ModelForm):
    jawaz_num = forms.IntegerField()
    statistic_num = forms.IntegerField()
    card_num = forms.IntegerField()
    document_num = forms.IntegerField()
    news_num = forms.IntegerField()
    bank_reg_num = forms.IntegerField()
    size = forms.IntegerField()
    rest_assured = forms.IntegerField()
    
    

    class Meta: 
        model = JawazSayr
        fields = '__all__'
        exclude = ['driver', 'car', 'verified_by', 'created']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'bank_reg_date': forms.DateInput(attrs={'type': 'date'}),
            'news_date': forms.DateInput(attrs={'type': 'date'}),
            'document_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    
    def __init__(self, *args, **kwargs):
        super(JawazForm, self).__init__(*args, **kwargs)
        
        for k, v in self.fields.items():
            v.widget.attrs.update(
                {'class':'input2', 
                }
                    )
            