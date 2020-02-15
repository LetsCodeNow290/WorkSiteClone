from django import forms
from .models import DailyCheck, NarcBox
from django.forms import formset_factory

class ChooseMedicUnit(forms.ModelForm):
    class Meta:
        model = DailyCheck
        fields = ['medic_unit_number']

class NarcSealForm(forms.ModelForm):
    class Meta:
        model = NarcBox
        fields = ['seal_number']
