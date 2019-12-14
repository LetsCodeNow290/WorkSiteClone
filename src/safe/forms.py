from django import forms
from .models import Safe
import django_filters

class DrugSearch(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date_created', lookup_expr='gte', label='Records After', widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}))
    exact_date = django_filters.DateFilter(field_name='date_created', lookup_expr='icontains', label='Records On', widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}))

    class Meta:
       model = Safe
       fields = ['drug_name', 'start_date', 'exact_date']


