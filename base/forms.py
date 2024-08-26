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

    def clean(self):
        cleaned_data = super().clean()
        url_1 = cleaned_data.get("url_1")
        url_2 = cleaned_data.get("url_2")

        if not url_1.startswith("https://"):
            self.add_error('url_1', "La URL debe comenzar con 'https://'")

        if not url_2.startswith("https://"):
            self.add_error('url_2', "La URL debe comenzar con 'https://'")

        if url_1 == url_2:
            raise ValidationError("Las URLs deben ser distintas.")

        return cleaned_data
