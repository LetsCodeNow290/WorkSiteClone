from django import forms
from .models import DailyCheck, NarcBox
from components.models import Drug
from django.forms import formset_factory, modelformset_factory, ModelChoiceField


class ChooseMedicUnit(forms.ModelForm):
    class Meta:
        model = DailyCheck
        fields = ['medic_unit_number']

class NarcSealForm(forms.ModelForm):
    class Meta:
        model = NarcBox
        fields = ['seal_number']

class NarcCheckForm(forms.ModelForm):
    class Meta:
        model = NarcBox
        fields = ['amount_in_unit', 'narc_box_free_text']

NarcCheckFormSet = modelformset_factory(NarcBox, form=NarcCheckForm, fields=('amount_in_unit', 'narc_box_free_text',), extra = len(Drug.objects.filter(is_active_unit=True)))

