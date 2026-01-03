# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.registerpage, name='register'),
    path('predict/', views.predict, name='predict'),
    path('details/', views.details, name='details'),
    path('save-details/', views.save_details, name='save_details'),
    
]
