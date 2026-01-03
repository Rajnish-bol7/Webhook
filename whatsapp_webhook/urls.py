"""
URL configuration for whatsapp_webhook project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook/', include('webhook.urls')),
    path('api/', include('webhook.api_urls')),
]

