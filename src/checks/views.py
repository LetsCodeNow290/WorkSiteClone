from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import DailyCheck, NarcBox

# Create your views here.
def check_home_view(request):
    return render(request, 'checks/checks_home.html')

class checkAdd(LoginRequiredMixin, CreateView):
    model = DailyCheck
    fields = ['medic_unit_number', 'unit_property_number', 'mileage', 'emergency_lights', 'driving_lights', 'red_bag', 'LP_15', 'BLS_bag', 'RTF_bag', 'suction', 'oxygen', 'free_text']
    success_url = '/checks'

    def form_valid(self, form):
        form.instance.daily_user = self.request.user
        return super().form_valid(form)

class NarcCheck(LoginRequiredMixin, CreateView):
    model = NarcBox
    fields = ['seal_number', 'narc_name', 'amount_in_unit', 'narc_box_free_text']
    success_url = '/checks'

def daily_view(request):
    return render(request, 'checks/daily_check.html')

def weekly_view(request):
    return render(request, 'checks/weekly_check.html')