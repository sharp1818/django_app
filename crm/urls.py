# crm/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.crm_dashboard, name='crm_dashboard'),
]