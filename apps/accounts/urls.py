# apps/accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('profile/', views.ProfileAPI.as_view(), name='profile'),
]