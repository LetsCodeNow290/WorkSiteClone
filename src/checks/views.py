from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import DailyCheck, NarcBox
from .forms import ChooseMedicUnit, NarcSealForm
from django.forms.models import model_to_dict
from django.http import JsonResponse
from components.models import MedicUnit

# Create your views here.
def check_home_view(request):
    if request.method == 'POST':
        form = ChooseMedicUnit(request.POST or None)
        if form.is_valid():
            unit_name = form.cleaned_data.get('medic_unit_number')
            request.session['unit_name'] = model_to_dict(unit_name)
            print(request.session['unit_name']['id'])
            return redirect('daily')
    else:
        form = ChooseMedicUnit()
    return render(request, 'checks/checks_home.html', {'form':form})

class checkAdd(CreateView):
    model = DailyCheck
    fields = ['unit_property_number', 'mileage', 'emergency_lights', 'driving_lights', 'red_bag', 'LP_15', 'BLS_bag', 'RTF_bag', 'suction', 'oxygen', 'free_text']
    success_url = '/checks/narc_seal/'

    def form_valid(self, form):
        form.instance.daily_user = self.request.user
        form.instance.medic_unit_number = MedicUnit.objects.get(pk=self.request.session['unit_name']['id'])
        return super().form_valid(form)

def narc_seal_view(request):
    if request.method == 'POST':
        form = NarcSealForm(request.POST or None)
        if form.is_valid():
            seal_number = form.cleaned_data.get('seal_number')
            request.session['seal_number'] = seal_number
            print(request.session['seal_number'])
            return redirect('narc_daily')
    else:
        form = NarcSealForm()
    return render(request, 'checks/narc_seal.html', {'form':form})

class NarcCheckAdd(CreateView):
    model = NarcBox
    fields = ['seal_number', 'narcotic_name', 'amount_in_unit', 'narc_box_free_text']    
    template_name_suffix = '_narc_daily'
    success_url = '/checks/narc_daily'

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['seal_number'] = self.request.session(['seal_number'])
    #     return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.narc_medic_unit_number = MedicUnit.objects.get(pk=self.request.session['unit_name']['id'])
        return super().form_valid(form)

def daily_view(request):
    return render(request, 'checks/daily_check.html')

def weekly_view(request):
    return render(request, 'checks/weekly_check.html')