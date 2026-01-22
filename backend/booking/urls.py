from django.urls import path 
from django.contrib.auth.views import LoginView

from .views import *

urlpatterns = [
    # rotas de autenticação e dashboard
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    # rotas do crud de serviços
    path("services/", ServiceListView.as_view(), name="service_list"),
    path("services/create/", ServiceCreateView.as_view(), name="service_create"),
    path("services/<int:pk>/edit/", ServiceUpdateView.as_view(), name="service_update"),
    path("services/<int:pk>/delete/", ServiceDeleteView.as_view(), name="service_delete")
]