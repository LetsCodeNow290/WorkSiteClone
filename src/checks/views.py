from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import DailyCheck, NarcBox,RSIBag
from .forms import ChooseMedicUnit, NarcSealForm, NarcCheckFormSet, RSICheckForm
from django.forms.models import model_to_dict
from django.http import JsonResponse
from components.models import MedicUnit, Drug


# Create your views here.
def check_home_view(request):
    if request.method == 'POST':
        form = ChooseMedicUnit(request.POST or None)
        if form.is_valid():
            unit_name = form.cleaned_data.get('medic_unit_number')
            request.session['unit_name'] = model_to_dict(unit_name)
            print(request.session['unit_name']['unit_name'])
            return redirect('daily')
    else:
        form = ChooseMedicUnit()
    return render(request, 'checks/checks_home.html', {'form':form})

class checkAdd(CreateView):
    model = DailyCheck
    fields = ['unit_property_number', 'mileage', 'emergency_lights', 'driving_lights', 'red_bag', 'LP_15', 'BLS_bag', 'RTF_bag', 'suction', 'oxygen', 'free_text']
    success_url = '/checks/narc_daily/'

    def form_valid(self, form):
        form.instance.daily_user = self.request.user
        form.instance.medic_unit_number = MedicUnit.objects.get(pk=self.request.session['unit_name']['id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['medic_unit'] = self.request.session['unit_name']['unit_name']
        return super().get_context_data(**kwargs)

#This is the new narc check form
def narc_check_view(request):
    if request.method == 'POST':
        if request.session['unit_name']['is_supervisor'] == True:
            RSI_check = RSICheckForm(request.POST or None)
            if RSI_check.is_valid():
                instance = RSI_check.save(commit=False)
                instance.user = request.user  
                instance.save()
        seal_form = NarcSealForm(request.POST or None)
        formset = NarcCheckFormSet(request.POST or None)
        drugset = Drug.objects.filter(is_active_unit=True)
          
        if formset.is_valid() and seal_form.is_valid():
            seal_number = seal_form.cleaned_data.get('seal_number')
            request.session['seal_number'] = seal_number
            count=0
            for form in formset:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.narc_medic_unit_number = MedicUnit.objects.get(pk=request.session['unit_name']['id'])
                instance.seal_number = request.session['seal_number']
                instance.narcotic_name = drugset[count]
                instance.save()
                count+=1
            formset.save()

        return redirect('check_home_view')
    else:
        display_unit = request.session['unit_name']['unit_name']
        context = {}
        if request.session['unit_name']['is_supervisor'] == True:
            RSI_check = RSICheckForm(request.POST or None)
            context.update({'RSI_check': RSI_check})
        seal_form = NarcSealForm(request.POST or None)
        # Notice below the "queryset" is equal to none. This is done so the only fields that render are the "extra" fields from the formset. Otherwise all of the old form records will populate.
        formset = NarcCheckFormSet(queryset=NarcBox.objects.none())
        drugset = Drug.objects.filter(is_active_unit=True)
        context.update({'formset':formset, 'drugset':drugset, 'seal_form':seal_form, 'display_unit':display_unit})
        
    return render(request, 'checks/narc_check.html', context)

def daily_view(request):
    return render(request, 'checks/daily_check.html')

def weekly_view(request):
    return render(request, 'checks/weekly_check.html')