from django.urls import path
from . import views

app_name = 'webhook'

urlpatterns = [
    path('', views.whatsapp_webhook, name='whatsapp_webhook'),
]

