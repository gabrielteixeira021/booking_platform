from django.urls import path 
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('register/', views.RegisterCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]