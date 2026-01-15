# fraudguard/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# SWAGGER & REDOC – VERSION CORRIGÉE ET RAPIDE
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="FraudGuard API",
      default_version='v1',
      description="Détection de fraude SMS & appels en temps réel – Cameroun",
      contact=openapi.Contact(email="contact@fraudguard.cm"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include('apps.api.urls')),
    path('api/fraud/', include('apps.fraud_detection.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/analytics/', include('apps.analytics.urls')),

    # SWAGGER & REDOC – CHAMP ÉDITABLE + CHARGEMENT RAPIDE
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)