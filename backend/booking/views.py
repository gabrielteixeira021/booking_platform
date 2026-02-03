from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .models import Service, Appointment
from .forms import CustomUserCreationForm, AppointmentForm


# Create your views here.

@method_decorator(login_required, name="dispatch")
class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"
    success_url = reverse_lazy("appointment_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.setdefault("initial", {})
        kwargs["initial"]["customer"] = self.request.user
        return kwargs
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        appointment = form.save(commit=False)
        appointment.customer = self.request.user
        appointment.save()
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class AppointmentListView(ListView):
    model = Appointment
    template_name = "appointments/appointment_list.html"
    context_object_name  = "appointments"
    def get_queryset(self):
        return Appointment.objects.filter(customer=self.request.user).order_by("start_time")
    

class RegisterCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user) # salva o cadastro pra logar automatiamente dps
        return super().form_valid(form)

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user,})

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


# Service CRUD views
@method_decorator(login_required, name="dispatch")
class ServiceListView(ListView):
    model = Service
    template_name = "services/service_list.html"
    context_object_name = "services"
    
@method_decorator(login_required, name="dispatch")
class ServiceCreateView(CreateView):
    model = Service
    fields = ["name", "description", "duration_minutes", "price", "is_active"]
    template_name = "services/service_form.html"
    success_url = reverse_lazy("service_list")
    

@method_decorator(login_required, name="dispatch")
class ServiceUpdateView(UpdateView):
    model = Service
    fields = ["name", "description", "duration_minutes", "price", "is_active"]
    template_name = "services/service_form.html"
    success_url = reverse_lazy("service_list")
    
@method_decorator(login_required, name="dispatch")
class ServiceDeleteView(DeleteView):
    model = Service
    template_name = "services/service_confirm_delete.html"
    success_url = reverse_lazy("service_list")
    
    
    
