# apps/accounts/urls_api.py
from django.urls import path
from .views import LoginAPI

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='v1-auth-login'),
]