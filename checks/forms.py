from django import forms
from .models import DailyCheck, NarcBox, RSIBag
from components.models import Drug
from django.forms import formset_factory, modelformset_factory, ModelChoiceField, Textarea, IntegerField


class ChooseMedicUnit(forms.ModelForm):
    class Meta:
        model = DailyCheck
        fields = ['medic_unit_number']

class NarcSealForm(forms.ModelForm):
    class Meta:
        model = NarcBox
        fields = ['seal_number']

class NarcCheckForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
        super(NarcCheckForm, self).__init__(*args, **kwargs)
        self.fields['amount_in_unit'].required = True
  class Meta:
      model = NarcBox
      fields = ['amount_in_unit']
      

NarcCheckFormSet = modelformset_factory(NarcBox, form=NarcCheckForm, fields=('amount_in_unit',), extra = len(Drug.objects.filter(is_active_unit=True)))

class RSICheckForm(forms.ModelForm):
    class Meta:
        model = RSIBag
        fields = ['RSI_seal_number','next_expiration_date','free_text']
        widgets = {
          'free_text': Textarea(attrs={'rows':2, 'cols':20}),
        }
        labels = {'free_text': 'RSI free text'}

class NarcBoxFreeText(forms.ModelForm):
  class Meta:
    model = NarcBox
    fields = ['narc_box_free_text']
    # widgets = {
    #     'narc_box_free_text': Textarea(attrs={'rows':2, 'cols':20}),
    #   }
    labels = {'narc_box_free_text' : 'Free Text'}

class SubDrugForm(forms.ModelForm):
  class Meta:
    model = NarcBox
    fields = [
        'narcotic_name',
        'amount_given_to_patient',
        'amount_removed_from_unit',
        'amount_added_to_unit',
        'incident_number',
        'hospital',
        'seal_number',
        'narc_box_free_text'
        ]
    labels = {
      'seal_number' : 'New seal number'
    }