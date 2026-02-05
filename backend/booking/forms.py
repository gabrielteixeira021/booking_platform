from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Appointment

class AppointmentForm(forms.ModelForm):
    """Formulário para realização do agendamentoo"""

    class Meta:
        model = Appointment
        fields = ["service", "start_time"]

        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
            "service": forms.Select(attrs={"class": "form-control"})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        # delega verificação de conflito para o model.clean()
        instance = Appointment(
            customer=self.initial.get("customer"),
            service=cleaned_data.get("service"),
            start_time=cleaned_data.get("start_time"),
        )
        # chama o metodo clean para validar  conflito/horário
        instance.clean()
        return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    """Formulario de cadastro personalizado"""

    username = forms.CharField(
        label="Nome de usuário",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome de usuário'
        })
    )

    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email'
        })
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )

    password2 = forms.CharField(
        label="Confirme a senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'digite sua senha novamente'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Traduzir mensagens de ajuda
        self.fields['username'].help_text = 'Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.'
        self.fields['password1'].help_text = 'Sua senha deve conter pelo menos 8 caracteres e não pode ser muito comum.'
        self.fields['password2'].help_text = 'Digite a mesma senha para verificação.'

class CustomAuthenticationForm(AuthenticationForm):
    """Formulário de login personalizado"""

    username = forms.CharField(
        label="Nome de usuário", 
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome de usuário'
        })
    )

    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )