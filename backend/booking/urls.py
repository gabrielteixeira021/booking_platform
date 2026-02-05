from django.urls import path 
from django.contrib.auth.views import LoginView

from .views import *
from .forms import CustomAuthenticationForm

urlpatterns = [
    # rotas de autenticação e dashboard
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    # rotas do crud de serviços
    path("services/", ServiceListView.as_view(), name="service_list"),
    path("services/create/", ServiceCreateView.as_view(), name="service_create"),
    path("services/<int:pk>/edit/", ServiceUpdateView.as_view(), name="service_update"),
    path("services/<int:pk>/delete/", ServiceDeleteView.as_view(), name="service_delete"),
]

# fluxo de agendamento
urlpatterns += [
    path("appointments/", appointment_list_view, name="appointment_list"),
    path("appointments/new/", appointment_create_view, name="appointment_create"),
]