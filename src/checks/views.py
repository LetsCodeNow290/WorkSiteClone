from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import DailyCheck

# Create your views here.
def check_home_view(request):
    return render(request, 'checks/checks_home.html')

class checkAdd(LoginRequiredMixin, CreateView):
    model = DailyCheck
    fields = ['medic_unit_number', 'unit_property_number']

def daily_view(request):
    return render(request, 'checks/daily_check.html')

def weekly_view(request):
    return render(request, 'checks/weekly_check.html')