from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import MedicUnit, Drug, Vehicle
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, VehicleAddForm, DrugAddForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
import os


@login_required
def component_home_view(request):
    return render(request, 'components/manage.html')

@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            property_number = form.cleaned_data.get('property_number')
            messages.success(request, f"Vehicle {property_number} added to the database")
            return redirect('component_home_view')
    else:
        form = VehicleAddForm()
    return render(request, 'components/vehicle_add.html', {'form': form})

class UnitListView(LoginRequiredMixin, ListView):
    model = Vehicle
    ordering = ['unit_number']

    def get_context_data(self, **kwargs):
        kwargs['mileage_list'] = Vehicle.get_mileage(Vehicle)
        return super(UnitListView, self).get_context_data(**kwargs)

class UnitDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle


class UnitUpdateView(LoginRequiredMixin,UpdateView):
    model = Vehicle
    fields = ['unit_number', 'property_number', 'make', 'model', 'year', 'mileage', 'image']
    # This next line redirects the page to the blog home page.
    success_url = '/manage/medic_unit'

class MedicCreateView(LoginRequiredMixin, CreateView):
    model = MedicUnit
    fields = ['unit_name', 'is_active', 'is_supervisor']
    template_name_suffix = '_add'
    success_url = '/manage/medic_unit'

class MedicListView(LoginRequiredMixin, ListView):
    model = MedicUnit
    ordering = ['unit_name']

class MedicDetailView(LoginRequiredMixin, DetailView):
    model = MedicUnit

class MedicUpdateView(LoginRequiredMixin,UpdateView):
    model = MedicUnit
    fields = ['unit_name', 'is_active', 'is_supervisor']
    # This next line redirects the page to the blog home page.
    success_url = '/manage/medic_unit'

@login_required
def add_drug(request):
    if request.method == 'POST':
        form = DrugAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f"{name} added to the database")
            return redirect('component_home_view')
    else:
        form = DrugAddForm()
    return render(request, 'components/drug_add.html', {'form': form})

class DrugListView(LoginRequiredMixin, ListView):
    model = Drug

class DrugUpdateView(LoginRequiredMixin,UpdateView):
    model = Drug
    fields = ['image', 'is_active_safe', 'is_active_unit']
    # This next line redirects the page to the blog home page
    success_url = '/manage/drugs'


@login_required
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}, now you need to log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'components/register.html', {'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated.")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'components/profile.html', context)




