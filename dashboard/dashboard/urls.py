from django.contrib import admin
from django.urls import path, include

# Patrones de url para cargar el frontend y el backend
urlpatterns = [
    path('', include('frontend.urls')),
    path('', include('backend.urls')),
]
