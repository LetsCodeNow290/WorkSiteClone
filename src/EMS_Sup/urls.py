"""EMS_Sup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from blog.views import blog_view, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from home.views import home_view
from checks.views import checkAdd, NarcCheckAdd
from checks.views import check_home_view, narc_seal_view
from safe.views import check_safe_view, safe_home_view, AddDrug, SubDrug, CheckDrug, search_drug
from components.views import component_home_view, add_drug, add_vehicle, profile, register, UnitUpdateView, UnitListView, UnitDetailView, DrugListView, DrugUpdateView, MedicCreateView, MedicListView



urlpatterns = [
    path('blog/', PostListView.as_view(), name='blog'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user_posts'),
    path('blog/new/', PostCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/update/', PostUpdateView.as_view(), name='blog_update'),
    path('blog/<int:pk>/delete/', PostDeleteView.as_view(), name='blog_delete'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='blog_detail'),
    path('', home_view, name='home'),
    path('login/', LoginView.as_view(template_name='components/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='components/logout.html'), name='logout'),
    path('checks/', check_home_view, name='check_home_view'),
    path('checks/daily/', checkAdd.as_view(), name='daily'),
    path('checks/narc_seal/', narc_seal_view, name='narc_seal'),
    path('checks/narc_daily/', NarcCheckAdd.as_view(), name='narc_daily'),
    #path('checks/weekly/', weekly_view, name='weekly'),
    path('safe/', safe_home_view, name='safe_home_view'),
    #path('safe/check/', CheckDrug.as_view(), name='safe_check_view'),
    #path('safe/check/', SafeCheck.as_view(), name='safe_check_view'),
    path('safe/check/', check_safe_view, name='safe_check_view'),
    path('safe/add/', AddDrug.as_view(), name='safe_add_view'),
    path('safe/remove/', SubDrug.as_view(), name='safe_remove_view'),
    path('safe/search/', search_drug, name='safe_search_view'),
    path('manage/', component_home_view, name='component_home_view'),
    path('manage/medic_unit/create/', MedicCreateView.as_view(), name='medic_unit_add'),
    path('manage/medic_unit/', MedicListView.as_view(), name='medic_unit'),
    path('manage/vehicle/', UnitListView.as_view(), name='vehicle'),
    path('manage/vehicle/<int:pk>/', UnitDetailView.as_view(), name='vehicle_detail'),
    path('manage/vehicle/add/', add_vehicle, name='vehicle_add'),
    path('manage/vehicle/<int:pk>/update/', UnitUpdateView.as_view(), name='vehicle_update'),
    path('manage/drugs/<int:pk>/update/', DrugUpdateView.as_view(), name='drug_update'),
    path('manage/drugs/add/', add_drug, name='add_drug'),
    path('manage/drugs/', DrugListView.as_view(), name='drugs'),
    path('profile/', profile, name='profile'),
    path('manage/register/', register, name='register'),
    path('admin/', admin.site.urls, name='admin'),
]

#This line ensures that media files are stored and accessed differently during development. Once production starts, debug mode will end and this line will be ignored
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)