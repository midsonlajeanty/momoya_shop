from typing import Any
from django import forms

from .models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = ['shipping', 'address', 'city', 'state', 'zipcode', 'country']
        widgets = {
            'shipping': forms.HiddenInput(),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'address': 'Address',
            'city': 'City',
            'state': 'State',
            'zipcode': 'Zipcode',
            'country': 'Country',
        }


