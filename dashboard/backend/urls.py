from django.urls import path
from . import views

urlpatterns = [
    path('api/search/', views.SearchListCreate.as_view() ),
]