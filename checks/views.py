from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import DailyCheck, NarcBox,RSIBag, WeeklyCheck
from .forms import ChooseMedicUnit, NarcSealForm, NarcCheckFormSet, RSICheckForm, NarcBoxFreeText, SubDrugForm
from django.forms.models import model_to_dict
from django.http import JsonResponse
from components.models import MedicUnit, Drug
from blog.models import Post


# Create your views here.
def check_home_view(request):
    if request.method == 'POST':
        form = ChooseMedicUnit(request.POST or None)
        if form.is_valid():
            unit_name = form.cleaned_data.get('medic_unit_number')
            request.session['unit_name'] = model_to_dict(unit_name)
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
            try:
                text_instance.narcotic_name = Drug.objects.get(name="Free Text")
            except:
                Drug.objects.create(name='Free Text', is_active_safe=False, is_active_unit=False)
                text_instance.narcotic_name = Drug.objects.get(name="Free Text")
            textset.save()

        return redirect('post_unit_view')
    else:
        display_unit = request.session['unit_name']['unit_name']
        context = {}
        if request.session['unit_name']['is_supervisor'] == True:
            RSI_check = RSICheckForm(request.POST or None)
            context.update({'RSI_check': RSI_check})
        seal_form = NarcSealForm(request.POST or None)
        # Notice below the "queryset" is equal to none. This is done so the only fields that render are the "extra" fields from the formset. Otherwise all of the old form records will populate.
        try:
            formset = NarcCheckFormSet(queryset=NarcBox.objects.none())
        except:
            formset = NarcBox.objects.none()
        drugset = Drug.objects.filter(is_active_unit=True)
        textset = NarcBoxFreeText()
        try:
            seal_number = NarcBox.objects.filter(narc_medic_unit_number=request.session['unit_name']['id']).order_by('-pk')[0]
        except:
            seal_number = 0
        try:
            RSI_seal_number = RSIBag.objects.order_by('pk')[0]
        except:
            RSI_seal_number = 0
        context.update({'formset':formset, 'drugset':drugset, 'seal_form':seal_form, 'display_unit':display_unit, 'textset' : textset, 'seal_number':seal_number, 'RSI_seal_number':RSI_seal_number})
        
    return render(request, 'checks/narc_check.html', context)

def post_unit_view(request):
    medic = request.session['unit_name']['unit_name']
    context={}
    try:
        pass_on = Post.objects.filter(title=request.session['unit_name']['unit_name']).last()
        context['pass_on'] = pass_on
    except:
        pass
    try:
        weekly = WeeklyCheck.objects.filter(weekly_unit_number=request.session['unit_name']['id']).order_by('-pk')[0]
        context['weekly'] = weekly
    except:
        pass
    try:
        daily_info = DailyCheck.objects.filter(medic_unit_number=request.session['unit_name']['id']).order_by('-pk')[0]        
        try:
            second_daily_info = DailyCheck.objects.filter(medic_unit_number=request.session['unit_name']['id']).order_by('-pk')[1]
            context.update({'daily_info':daily_info, 'second_daily_info':second_daily_info, 'medic':medic})
        except:
            context.update({'daily_info':daily_info, 'medic':medic})
    except:
        context.update({'medic':medic})
    return render(request, 'checks/post_unit_view.html', context)

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
    success_url = '/checks/home/'
    template_name = 'checks/weekly_check_view.html'
    
    def form_valid(self, form):
        form.instance.weekly_user = self.request.user
        form.instance.weekly_unit_number = MedicUnit.objects.get(pk=self.request.session['unit_name']['id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['medic_unit'] = self.request.session['unit_name']['unit_name']
        return super().get_context_data(**kwargs)

    def get_form(self, form_class=None):
        form = super(WeeklyCheckView, self).get_form(form_class)
        form.fields['comments'].required = True
        return form

class AddDrugNarcBox(CreateView):
    model = NarcBox
    template_name_suffix = '_add_narc'
    fields = ['narcotic_name', 'amount_added_to_unit', 'seal_number','narc_box_free_text']
    success_url = '/checks/home'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.narc_medic_unit_number = MedicUnit.objects.get(pk=self.request.session['unit_name']['id'])
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super(AddDrugNarcBox, self).get_form(form_class)
        form.fields['amount_added_to_unit'].required = True
        return form

class SubDrugNarcBox(CreateView):
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
    #form_class = SubDrugForm
    success_url = '/checks/home'
    template_name_suffix = '_sub_narc'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.narc_medic_unit_number = MedicUnit.objects.get(pk=self.request.session['unit_name']['id'])
        return super().form_valid(form)
        
    # This bit of code is making the "amount removed" category required
    def get_form(self, form_class=None):
        form = super(SubDrugNarcBox, self).get_form(form_class)
        form.fields['amount_removed_from_unit'].required = True
        form.fields['amount_added_to_unit'].required = True
        return form
