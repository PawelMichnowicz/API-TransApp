from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.LoginApi.as_view()),
    path('check/', views.TestApi.as_view()), 
    path('refresh/', views.RefreshApi.as_view()),
    path('register/', views.RegisterApi.as_view()),
]   



