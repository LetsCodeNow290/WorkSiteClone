from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, MedicUnit, Drug, Vehicle

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class VehicleAddForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['unit_number', 'property_number', 'year', 'make', 'model', 'mileage']

class DrugAddForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'is_active_safe', 'is_active_unit']

