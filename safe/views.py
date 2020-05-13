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
from .forms import DrugSearch, SafeCheckFormSet, SafeCheckForm, SafeCheckFreeText
import django_filters
from extra_views import ModelFormSetView

# Create your views here.


@login_required
@permission_required('safe.can_view')
def safe_home_view(request):
    drugs = Safe.calc_total(Safe)
    checked = Safe.objects.last()
    context = {'drugs' : drugs, 'checked': checked}
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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        
# This bit of code is making the "amount removed" category required
    def get_form(self, form_class=None):
        form = super(SubDrug, self).get_form(form_class)
        form.fields['amount_removed'].required = True
        return form

class CheckDrug(LoginRequiredMixin,CreateView):
    model = Safe
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
        drugset = Drug.objects.filter(is_active_safe=True)
        textset = SafeCheckFreeText(request.POST)
        if formset.is_valid() and textset.is_valid():
            count = 0
            # This next for loop adds the user and the drug name automaticlly 
            for form in formset:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.drug_name = drugset[count]
                instance.save()
                count+=1
            formset.save()
            text_instance = textset.save(commit=False)
            text_instance.user = request.user
            text_instance.drug_name = Drug.objects.get(name="Free Text")
            textset.save()

        return redirect('safe_home_view')
    else:
        #These next datasets will send the correct drug name and form to the template
        formset = SafeCheckFormSet(queryset=Safe.objects.none())
        drugs = Drug.objects.filter(is_active_safe=True)
        object_list = Safe.calc_total(Safe)
        drugset = {}
        for drug in drugs:
            for total in object_list:
                if drug == total:
                    drugset.update({f'{drug}: {object_list[drug]}mg': drug})
        date_list = Safe.get_check_date(Safe)
        text_box = SafeCheckFreeText()
        context = {'formset': formset, 'drugset' : drugset, 'object_list' : object_list, 'date_list': date_list, 'text_box' : text_box}
       
    return render(request, template_name, context)

@login_required
def search_drug(request):
    form = DrugSearch(request.GET, queryset=Safe.objects.all().order_by('-date_created'))
    return render(request, 'safe/safe_search.html', {'filter' : form })


