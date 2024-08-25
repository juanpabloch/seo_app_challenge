from django import forms 
from django.core import validators
from django.core.exceptions import ValidationError

class UrlSelectionForm(forms.Form):
    CHOICES = (('desktop', 'Desktop'),('mobile', 'Mobile'),)
    
    url_1 = forms.URLField(
        required=True,
        label='Enter a URL to compare speed',
        widget=forms.TextInput(attrs={'placeholder': 'https://example.com'}),
        validators=[validators.MinLengthValidator(8)]
    )
     
    url_2 = forms.URLField(
        required=True,
        label='Enter a second URL to compare speed',
        widget=forms.TextInput(attrs={'placeholder': 'https://example.com'}),
        validators=[validators.MinLengthValidator(8)]
    ) 

    strategy = forms.ChoiceField(choices=CHOICES, label="Select a mode, default is Desktop")

    def clean_url_1(self):
        url = self.cleaned_data.get('url_1')
        
        if not url.startswith("https://"):
            raise ValidationError("La URL debe comenzar con 'https://'")

        return url

    def clean_url_2(self):
        url = self.cleaned_data.get('url_2')
        
        if not url.startswith("https://"):
            raise ValidationError("La URL debe comenzar con 'https://'")

        return url