from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import MedicUnit, Drug
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UnitAddForm, DrugAddForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


@login_required
def component_home_view(request):
    return render(request, 'components/manage.html')

@login_required
def add_medic_unit(request):
    if request.method == 'POST':
        form = UnitAddForm(request.POST or None)
        if form.is_valid():
            form.save()
            unit_number = form.cleaned_data.get('unit_number')
            messages.success(request, f"Medic {unit_number} added to the database")
            return redirect('component_home_view')
    else:
        form = UnitAddForm()
    return render(request, 'components/medicunit_add.html', {'form': form})

class UnitListView(LoginRequiredMixin, ListView):
    model = MedicUnit
    ordering = ['unit_number']

class UnitDetailView(LoginRequiredMixin, DetailView):
    model = MedicUnit


class UnitUpdateView(LoginRequiredMixin,UpdateView):
    model = MedicUnit
    fields = ['property_number', 'make', 'model', 'year', 'mileage', 'image']
    # This next line redirects the page to the blog home page. Right now it doesn't work because the url will not reset
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
    fields = ['image', 'is_active']
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




