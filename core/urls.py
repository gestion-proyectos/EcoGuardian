from django.contrib import admin
from django.urls import path, include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='registro'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
]
