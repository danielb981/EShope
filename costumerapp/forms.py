from django import forms
from .models import Costumer


class CostumerForm(forms.ModelForm):
    class Meta:
        model = Costumer
        fields = [
            'name',
            'age',
            'gender',
        ]