from django import forms
from .models import Crime

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
    
    