from django import forms
from .models import Bounty

class BountyForm(forms.ModelForm):
    class Meta:
        model = Bounty
        fields = ['objective', 'reward', 'tier']
