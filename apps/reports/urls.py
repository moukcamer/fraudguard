# apps/reports/urls.py
from django.urls import path
from .views import ReportCreateView, ReportListView

urlpatterns = [
    path('submit/', ReportCreateView.as_view(), name='submit_report'),
    path('my/', ReportListView.as_view(), name='my_reports'),
]