"""store_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from clients import views

app_name = 'clients'
urlpatterns = [
    path('', views.home, name='home'),
    path('add_client/', views.add_client, name='add_client'),
    path('update_client/<str:pk>/', views.update_client, name='update_client'),
    path('delete_client/<str:pk>/', views.delete_client, name='delete_client'),
    path('receipt/',views.receipt, name='receipt'),
    path('add_receipt/', views.add_receipt, name='add_receipt'),
    path('delete_receipt/<str:pk>/' ,views.delete_receipt, name='delete_receipt'),
]
