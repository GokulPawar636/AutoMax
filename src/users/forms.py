from dataclasses import field
from django import forms
from .models import Location


class LocationForm(forms.ModelForm):
    address_1 = forms.CharField(required=True)
    zipcode = forms.CharField(required=True)

    class Meta:
        model = Location
        fields = {'address_1', 'address_2', 'city', 'state', 'zipcode'}