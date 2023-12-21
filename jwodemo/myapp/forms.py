# myapp/forms.py

from django import forms
from django.core.validators import MaxLengthValidator

class CoinMessageForm(forms.Form):
    coin_message = forms.CharField(
        max_length=100,
        validators=[MaxLengthValidator(limit_value=100, message='Exceeded maximum length of 100 characters.')]
    )
