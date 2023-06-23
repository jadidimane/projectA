from django.urls import path
from .views import candidature,candidature_success

urlpatterns = [
    path('candidature/', candidature, name='candidatur'),
    path('candidature/success/', candidature_success, name='candidature_avec_succes'),
]