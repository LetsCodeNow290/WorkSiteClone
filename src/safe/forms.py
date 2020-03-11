from django import forms
from .models import Safe
from components.models import Drug
import django_filters
from django.forms import modelformset_factory, ModelChoiceField, Textarea

class DrugSearch(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date_created', lookup_expr='gte', label='Records After', widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}))
    exact_date = django_filters.DateFilter(field_name='date_created', lookup_expr='icontains', label='Records On', widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}))

    class Meta:
       model = Safe
       fields = ['drug_name', 'start_date', 'exact_date']

class SafeCheckForm(forms.ModelForm):
    class Meta:
        model = Safe
        fields = ['amount_in_safe']
        widgets = {
          'free_text': Textarea(attrs={'rows':2, 'cols':20}),
        }

SafeCheckFormSet = modelformset_factory(Safe, form=SafeCheckForm, fields=('amount_in_safe',), extra = len(Drug.objects.filter(is_active_safe=True)))

class SafeCheckFreeText(forms.ModelForm):
  class Meta:
    model = Safe
    fields = ['free_text']