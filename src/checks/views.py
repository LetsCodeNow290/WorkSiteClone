from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import DailyCheck, NarcBox,RSIBag, WeeklyCheck
from .forms import ChooseMedicUnit, NarcSealForm, NarcCheckFormSet, RSICheckForm, NarcBoxFreeText
from django.forms.models import model_to_dict
from django.http import JsonResponse
from components.models import MedicUnit, Drug
from django.db.models import Sum, Max


# Create your views here.
def check_home_view(request):
    if request.method == 'POST':
        form = ChooseMedicUnit(request.POST or None)
        if form.is_valid():
            unit_name = form.cleaned_data.get('medic_unit_number')
            request.session['unit_name'] = model_to_dict(unit_name)
            print(request.session['unit_name']['unit_name'])
            return redirect('post_unit_view')
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
        textset = NarcBoxFreeText(request.POST or None)
          
        if formset.is_valid() and seal_form.is_valid() and textset.is_valid():
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
            text_instance = textset.save(commit=False)
            text_instance.user = request.user
            text_instance.narc_medic_unit_number = MedicUnit.objects.get(pk=request.session['unit_name']['id'])
            text_instance.seal_number = request.session['seal_number']
            text_instance.narcotic_name = Drug.objects.get(name="Free Text")
            textset.save()

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
        textset = NarcBoxFreeText()
        context.update({'formset':formset, 'drugset':drugset, 'seal_form':seal_form, 'display_unit':display_unit, 'textset' : textset})
        
    return render(request, 'checks/narc_check.html', context)

def post_unit_view(request):
    daily_info = DailyCheck.objects.latest('free_text')
    return render(request, 'checks/post_unit_view.html',{'daily_info':daily_info})

class WeeklyCheckView(CreateView):
    model = WeeklyCheck
    fields = [
        'engine_oil',
        'transmission_fluid',
        'brake_fluid',
        'coolant',
        'LUCAS_device',
        'EMS_equipment',
        'suciton_unit',
        'driver_front_tire',
        'driver_rear_tire',
        'passenger_front_tire',
        'passenger_rear_tire',
        'comments'
    ]
    success_url = '/checks/'
    template_name = 'checks/weekly_check_view.html'
    
    def form_valid(self, form):
        form.instance.weekly_user = self.request.user
        form.instance.weekly_unit_number = MedicUnit.objects.get(pk=self.request.session['unit_name']['id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['medic_unit'] = self.request.session['unit_name']['unit_name']
        return super().get_context_data(**kwargs)