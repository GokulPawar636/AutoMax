from dataclasses import field
from django import forms
from .models import Location
from django.contrib.auth.models import User
from .models import Location, Profile

class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('photo', 'bio','phone_number')
        

class LocationForm(forms.ModelForm):
    address_1 = forms.CharField(required=True)
    zipcode = forms.CharField(required=True)

    class Meta:
        model = Location
        fields = {'address_1', 'address_2', 'city', 'state', 'zipcode'}