from django import forms
from .models import Safe
import django_filters

class DrugSearch(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date_created', lookup_expr='gte', label='Records After')
    exact_date = django_filters.DateFilter(field_name='date_created', lookup_expr='icontains', label='Records On')

    class Meta:
       model = Safe
       fields = ['drug_name', 'start_date', 'exact_date']


