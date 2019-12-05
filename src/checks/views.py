from django.shortcuts import render

# Create your views here.
def check_home_view(request):
    return render(request, 'checks/checks_home.html')

def daily_view(request):
    return render(request, 'checks/daily_check.html')

def weekly_view(request):
    return render(request, 'checks/weekly_check.html')