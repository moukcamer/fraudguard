# apps/analytics/urls.py
from django.urls import path
from .views import DashboardStatsView

# ON SUPPRIME app_name TOTALEMENT → plus de namespace du tout
# app_name = 'analytics'   ← SUPPRIMÉ !

urlpatterns = [
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard'),
]