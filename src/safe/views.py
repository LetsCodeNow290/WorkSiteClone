from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from components.models import Drug
from .models import Safe
from django.db.models import Sum, Q
from django.template import RequestContext
from django.forms import modelformset_factory
from django.db import transaction
from .forms import DrugSearch, SafeCheckFormSet
import django_filters
from extra_views import ModelFormSetView




# Create your views here.


@login_required
@permission_required('safe.can_view')
def safe_home_view(request):
    drugs = Safe.calc_total(Safe)
    context = {'drugs' : drugs}
    return render(request, 'safe/safe_home.html', context)

class AddDrug(LoginRequiredMixin, PermissionRequiredMixin ,CreateView, AccessMixin):
    permission_required = ('can_add',)
    raise_exception = False
    model = Safe
    template_name_suffix = '_add'
    fields = ['drug_name', 'amount_added', 'free_text']
    required = ['amount_added']
    success_url = '/safe'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super(AddDrug, self).get_form(form_class)
        form.fields['amount_added'].required = True
        return form

class SubDrug(LoginRequiredMixin,CreateView):
    model = Safe
    template_name_suffix = '_sub'
    fields = [
        'drug_name', 
        'amount_removed', 
        'incident_number', 
        'patient_name', 
        'medic_unit', 
        'free_text'
        ]
    success_url = '/safe'
# These bits of code are making the "amount removed" category required
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super(SubDrug, self).get_form(form_class)
        form.fields['amount_removed'].required = True
        return form

class CheckDrug(LoginRequiredMixin,CreateView):
    model = Safe
    form = SafeCheckFormSet(queryset=Drug.objects.filter(is_active_safe=True))
    template_name_suffix = '_check'
    fields = ['drug_name', 'amount_in_safe', 'free_text']
    required = ['amount_in_safe']
    success_url = '/safe/check'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Safe.calc_total(Safe)
        kwargs['date_list'] = Safe.get_check_date(Safe)
        return super(CheckDrug, self).get_context_data(**kwargs)

    def get_form(self, form_class=None):
        form = super(CheckDrug, self).get_form(form_class)
        form.fields['amount_in_safe'].required = True
        return form


def check_safe_view(request):
    template_name = 'safe/safe_check_formset.html'
    if request.method == 'POST':
        formset = SafeCheckFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('amount_in_safe'):
                    form.save()
        return redirect('safe_home_view')
    else:
        # count = 0
        # queryset = {}
        # for drug in Drug.objects.filter(is_active_safe=True):
        #     print(drug)
        #     queryset.update({drug.key(): drug})
        #     count+=1
        # print(queryset)
        formset = SafeCheckFormSet(queryset=Drug.objects.filter(is_active_safe=True))
        # formset = SafeCheckFormSet(queryset=Drug.objects.filter(is_active_safe=True))
        # count = 0
        # for form in formset:
        #     form.fields['drug_name'] = form.fields['drug_name'].queryset[count]
            
        #     count+=1
    return render(request, template_name, {'formset':formset})

@login_required
def search_drug(request):
    form = DrugSearch(request.GET, queryset=Safe.objects.all().order_by('-date_created'))
    return render(request, 'safe/safe_search.html', {'filter' : form })


