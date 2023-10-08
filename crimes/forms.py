from django import forms
from .models import Crime, CarCrime

class CreateCrimeForm(forms.ModelForm):
    class Meta:
        model = Crime
        fields = ['title', 'description', 'min_price', 'max_price']
        labels = {
            'title': 'موضوع جریمه', 
            'description': 'ملاحظات',
            'min_price': 'حداقل مبلغ جریمه',
            'max_price': 'حداکثر مبلغ جریمه'
        }

    def clean(self):
        cleaned_data = super().clean()
        max_price = cleaned_data.get('max_price')
        min_price = cleaned_data.get('min_price')
        
        if min_price and max_price and max_price < min_price :
            raise forms.ValidationError('حداقل مبلغ جریمه باید کوچکتر از حداکثر مبلغ جریمه باشد')
        
        return cleaned_data
    

class CreateCarCrimeForm(forms.ModelForm):
    plate_num = forms.CharField(max_length=200, required=True)
    class Meta:
        model = CarCrime
        fields = [
            'plate_num', 'crime', 'location', 'description', 'paid', 'price', 'expiry_date'
        ]