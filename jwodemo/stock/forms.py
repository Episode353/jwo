from django import forms
from .models import Stock

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'color']  # Exclude 'value' and 'last_updated'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color'].widget = forms.TextInput(attrs={'type': 'color'})
