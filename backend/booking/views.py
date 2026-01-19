from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse 
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# Create your views here.
class RegisterCreateView(CreateView):
    form_class = UserCreationForm
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
