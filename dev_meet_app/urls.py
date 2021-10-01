from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<int:pk>/', views.rooms, name='room'),
]