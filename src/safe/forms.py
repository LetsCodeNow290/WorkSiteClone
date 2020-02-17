from django import forms
from .models import Safe
from components.models import Drug
import django_filters
from django.forms import modelformset_factory, ModelChoiceField

class DrugSearch(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date_created', lookup_expr='gte', label='Records After', widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}))
    exact_date = django_filters.DateFilter(field_name='date_created', lookup_expr='icontains', label='Records On', widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}))

    class Meta:
       model = Safe
       fields = ['drug_name', 'start_date', 'exact_date']

# class DrugNameModelField(ModelChoiceField):
#     def label_from_instance(self, obj):
#         return f'{obj.drug_name}'

SafeCheckFormSet = modelformset_factory(Safe, fields=('drug_name','amount_in_safe',), extra = 0)
