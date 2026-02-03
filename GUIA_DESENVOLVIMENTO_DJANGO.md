# Guia de Desenvolvimento Django - Padrões e Boas Práticas

## 📚 Índice
1. [Arquitetura MVT](#arquitetura-mvt)
2. [Padrão de Desenvolvimento CRUD](#padrão-crud)
3. [Fluxo de Dados](#fluxo-de-dados)
4. [Exemplos Práticos](#exemplos-práticos)
5. [Validações e Regras de Negócio](#validações)
6. [Formulários Personalizados](#formulários)

---

## 🏗️ Arquitetura MVT

Django utiliza o padrão **MVT (Model-View-Template)**, uma variação do MVC:

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────┐
│   URLs      │ ← Roteamento (urls.py)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Views     │ ← Lógica de Negócio (views.py)
└──────┬──────┘
       │
       ├─────────────┐
       ▼             ▼
┌─────────────┐ ┌─────────────┐
│   Models    │ │  Templates  │
│ (models.py) │ │   (.html)   │
└─────────────┘ └─────────────┘
       │             │
       ▼             ▼
┌─────────────┐ ┌─────────────┐
│  Database   │ │  HTML/CSS   │
└─────────────┘ └─────────────┘
```

---

## 🔄 Padrão de Desenvolvimento CRUD

Todo recurso no Django segue o mesmo padrão de 4 camadas:

### 1️⃣ **MODEL** - Estrutura de Dados
Define a estrutura da tabela no banco de dados e regras de validação.

#### Exemplo: Service (Serviço)
```python
# booking/models.py
class Service(models.Model):
    # CAMPOS (colunas do banco)
    name = models.CharField(_("nome"), max_length=100)
    description = models.TextField(_("descrição"), blank=True)
    duration_minutes = models.PositiveIntegerField(_("duração (min)"))
    price = models.DecimalField(_("preço"), max_digits=8, decimal_places=2)
    is_active = models.BooleanField(_("está ativo"), default=True)

    # REPRESENTAÇÃO
    def __str__(self):
        return self.name
```

#### Exemplo: Appointment (Agendamento)
```python
class Appointment(models.Model):
    # RELACIONAMENTOS (Foreign Keys)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    
    # CAMPOS
    start_time = models.DateTimeField(_("início do serviço"))
    end_time = models.DateTimeField(_("término do serviço"))
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default="pending"
    )
    
    # VALIDAÇÕES (executadas antes de salvar)
    def clean(self):
        # Valida se horário não é no passado
        if self.start_time < timezone.now():
            raise ValidationError("Não é possível agendar no passado")
        
        # Calcula end_time automaticamente
        if not self.end_time:
            self.end_time = self.start_time + timedelta(
                minutes=self.service.duration_minutes
            )
        
        # Valida conflitos de horário
        overlap = Appointment.objects.filter(
            service=self.service,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exists()
        
        if overlap:
            raise ValidationError("Já existe um agendamento nesse horário")
    
    # METADATA
    class Meta:
        ordering = ["-start_time"]  # Ordenação padrão
```

**Padrão que se repete:**
- ✅ Campos básicos definem estrutura
- ✅ ForeignKey para relacionamentos
- ✅ `__str__()` para representação
- ✅ `clean()` para validações customizadas
- ✅ `Meta` para configurações

---

### 2️⃣ **FORMS** - Validação de Input

Formulários processam e validam dados do usuário.

#### Formulário Simples (ModelForm)
```python
# booking/forms.py
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["service", "start_time"]
        
        # Personalizar widgets (campos HTML)
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
            "service": forms.Select(attrs={"class": "form-control"})
        }
    
    # Validação customizada
    def clean(self):
        cleaned_data = super().clean()
        
        # Criar instância temporária para validar
        instance = Appointment(
            customer=self.initial.get("customer"),
            service=cleaned_data.get("service"),
            start_time=cleaned_data.get("start_time"),
        )
        
        # Delega validação para o model
        instance.clean()
        
        return cleaned_data
```

#### Formulário de Autenticação
```python
class CustomUserCreationForm(UserCreationForm):
    # Sobrescrever campos para personalizar
    username = forms.CharField(
        label="Nome de usuário",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome de usuário'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customizar mensagens de ajuda
        self.fields['password1'].help_text = 'Sua senha deve conter pelo menos 8 caracteres'
```

**Padrão que se repete:**
- ✅ Herda de `ModelForm` para CRUD
- ✅ Define `model` e `fields` no Meta
- ✅ Usa `widgets` para personalizar HTML
- ✅ `clean()` para validações customizadas
- ✅ `__init__()` para personalizações avançadas

---

### 3️⃣ **VIEWS** - Lógica de Negócio

Views processam requisições e retornam respostas.

#### Class-Based Views (CBV) - Padrão Recomendado

```python
# booking/views.py

# === PADRÃO CRUD COMPLETO ===

# CREATE (Criar novo registro)
@method_decorator(login_required, name="dispatch")
class ServiceCreateView(CreateView):
    model = Service
    fields = ["name", "description", "duration_minutes", "price", "is_active"]
    template_name = "services/service_form.html"
    success_url = reverse_lazy("service_list")

# READ (Listar registros)
@method_decorator(login_required, name="dispatch")
class ServiceListView(ListView):
    model = Service
    template_name = "services/service_list.html"
    context_object_name = "services"
    
    # Filtrar queryset
    def get_queryset(self):
        return Service.objects.filter(is_active=True)

# UPDATE (Editar registro)
@method_decorator(login_required, name="dispatch")
class ServiceUpdateView(UpdateView):
    model = Service
    fields = ["name", "description", "duration_minutes", "price", "is_active"]
    template_name = "services/service_form.html"
    success_url = reverse_lazy("service_list")

# DELETE (Deletar registro)
@method_decorator(login_required, name="dispatch")
class ServiceDeleteView(DeleteView):
    model = Service
    template_name = "services/service_confirm_delete.html"
    success_url = reverse_lazy("service_list")
```

#### Personalização Avançada

```python
class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"
    success_url = reverse_lazy("appointment_list")

    # Passar dados iniciais para o formulário
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.setdefault("initial", {})
        kwargs["initial"]["customer"] = self.request.user
        return kwargs
    
    # Processar antes de salvar
    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.customer = self.request.user
        appointment.save()
        return super().form_valid(form)
```

#### Function-Based View (FBV) - Para casos simples

```python
@login_required
def dashboard(request):
    context = {
        'user': request.user,
        'appointments_today': Appointment.objects.filter(
            customer=request.user,
            start_time__date=timezone.now().date()
        ).count()
    }
    return render(request, 'dashboard.html', context)
```

**Padrão que se repete:**
- ✅ Define `model`, `template_name`, `success_url`
- ✅ `get_queryset()` para filtros customizados
- ✅ `get_form_kwargs()` para passar dados ao form
- ✅ `form_valid()` para processar antes de salvar
- ✅ Decorators para autenticação (`@login_required`)

---

### 4️⃣ **URLS** - Roteamento

Mapeia URLs para views.

```python
# booking/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # === PADRÃO CRUD ===
    # List
    path("services/", ServiceListView.as_view(), name="service_list"),
    # Create
    path("services/create/", ServiceCreateView.as_view(), name="service_create"),
    # Update (usa <int:pk> para capturar ID)
    path("services/<int:pk>/edit/", ServiceUpdateView.as_view(), name="service_update"),
    # Delete
    path("services/<int:pk>/delete/", ServiceDeleteView.as_view(), name="service_delete"),
    
    # === APPOINTMENTS ===
    path("appointments/", AppointmentListView.as_view(), name="appointment_list"),
    path("appointments/new/", AppointmentCreateView.as_view(), name="appointment_create"),
    
    # === AUTHENTICATION ===
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]
```

**Padrão que se repete:**
- ✅ Nomes descritivos: `service_list`, `service_create`, etc.
- ✅ Use `<int:pk>` para capturar IDs
- ✅ `.as_view()` para Class-Based Views
- ✅ `name=` para referência nos templates

---

### 5️⃣ **TEMPLATES** - Interface

Templates renderizam HTML dinâmico.

#### Template Base (Reutilizável)
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <title>{% block title %}Agendamentos{% endblock %}</title>
  {% load static %}
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container">
      <a class="navbar-brand" href="{% url 'dashboard' %}">Agendamentos</a>
      {% if user.is_authenticated %}
      <div class="navbar-nav ms-auto">
        <a class="nav-link" href="{% url 'dashboard' %}">Dashboard</a>
        <a class="nav-link" href="{% url 'service_list' %}">Serviços</a>
        <a class="nav-link" href="{% url 'appointment_list' %}">Agendamentos</a>
        <a class="nav-link" href="{% url 'logout' %}">Sair</a>
      </div>
      {% endif %}
    </div>
  </nav>

  <div class="container py-4">
    {% block content %}{% endblock %}
  </div>
</body>
</html>
```

#### Template de Lista (ListView)
```html
<!-- templates/services/service_list.html -->
{% extends "base.html" %}
{% block title %}Serviços{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2>Serviços</h2>
  <a href="{% url 'service_create' %}" class="btn btn-primary">+ Novo Serviço</a>
</div>

<table class="table">
  <thead>
    <tr>
      <th>Nome</th>
      <th>Duração</th>
      <th>Preço</th>
      <th>Ações</th>
    </tr>
  </thead>
  <tbody>
    {% for service in services %}
    <tr>
      <td>{{ service.name }}</td>
      <td>{{ service.duration_minutes }} min</td>
      <td>R$ {{ service.price }}</td>
      <td>
        <a href="{% url 'service_update' service.pk %}">Editar</a>
        <a href="{% url 'service_delete' service.pk %}">Deletar</a>
      </td>
    </tr>
    {% empty %}
    <tr><td colspan="4">Nenhum serviço cadastrado</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```

#### Template de Formulário (CreateView/UpdateView)
```html
<!-- templates/services/service_form.html -->
{% extends "base.html" %}
{% block title %}{% if object %}Editar{% else %}Novo{% endif %} Serviço{% endblock %}

{% block content %}
<h2>{% if object %}Editar{% else %}Novo{% endif %} Serviço</h2>

<form method="post">
  {% csrf_token %}
  
  {% for field in form %}
  <div class="mb-3">
    <label>{{ field.label }}</label>
    {{ field }}
    {% if field.errors %}
      <div class="text-danger">{{ field.errors }}</div>
    {% endif %}
  </div>
  {% endfor %}
  
  <button type="submit" class="btn btn-primary">Salvar</button>
  <a href="{% url 'service_list' %}" class="btn btn-secondary">Cancelar</a>
</form>
{% endblock %}
```

**Padrão que se repete:**
- ✅ `{% extends "base.html" %}` para herança
- ✅ `{% block content %}` para sobrescrever seções
- ✅ `{% url 'name' %}` para URLs dinâmicas
- ✅ `{% csrf_token %}` em todos os forms
- ✅ `{% for item in items %}` para loops
- ✅ `{{ variable }}` para exibir valores

---

## 🔁 Fluxo de Dados Completo

### Exemplo: Criar um novo agendamento

```
1. Usuário acessa: /appointments/new/
   ↓
2. urls.py mapeia para AppointmentCreateView
   ↓
3. View:
   - Cria instância do AppointmentForm
   - Passa user atual como initial data
   - Renderiza template
   ↓
4. Template exibe formulário HTML
   ↓
5. Usuário preenche e submete (POST)
   ↓
6. View recebe POST:
   - Valida form (form.is_valid())
   - Form.clean() valida campos
   - Model.clean() valida regras de negócio
   ↓
7. Se válido:
   - form_valid() processa dados
   - Salva no banco (model.save())
   - Redireciona para success_url
   ↓
8. Se inválido:
   - Re-renderiza form com erros
```

---

## 📋 Checklist de Desenvolvimento

Para criar qualquer nova funcionalidade:

### ✅ 1. Model
```python
class NovoModel(models.Model):
    # Campos
    campo = models.CharField(max_length=100)
    
    # Validação
    def clean(self):
        pass
    
    # Representação
    def __str__(self):
        return self.campo
    
    # Metadata
    class Meta:
        ordering = ['-id']
```

### ✅ 2. Form (se necessário)
```python
class NovoModelForm(forms.ModelForm):
    class Meta:
        model = NovoModel
        fields = ['campo1', 'campo2']
        widgets = {
            'campo1': forms.TextInput(attrs={'class': 'form-control'})
        }
```

### ✅ 3. Views (CRUD completo)
```python
class NovoModelListView(ListView):
    model = NovoModel
    template_name = "app/novomodel_list.html"
    context_object_name = "items"

class NovoModelCreateView(CreateView):
    model = NovoModel
    fields = ['campo1', 'campo2']
    template_name = "app/novomodel_form.html"
    success_url = reverse_lazy("novomodel_list")

# UpdateView, DeleteView...
```

### ✅ 4. URLs
```python
urlpatterns = [
    path('items/', NovoModelListView.as_view(), name='novomodel_list'),
    path('items/new/', NovoModelCreateView.as_view(), name='novomodel_create'),
    path('items/<int:pk>/edit/', NovoModelUpdateView.as_view(), name='novomodel_update'),
    path('items/<int:pk>/delete/', NovoModelDeleteView.as_view(), name='novomodel_delete'),
]
```

### ✅ 5. Templates
```
templates/
  app/
    novomodel_list.html
    novomodel_form.html
    novomodel_confirm_delete.html
```

### ✅ 6. Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🎯 Boas Práticas

### 1. Validações
- ✅ Use `model.clean()` para regras de negócio
- ✅ Use `form.clean()` para validações de formulário
- ✅ Use `field.validators` para validações de campo

### 2. Segurança
- ✅ Sempre use `{% csrf_token %}` em forms
- ✅ Use `@login_required` para proteger views
- ✅ Valide permissões no backend, não só no frontend

### 3. Performance
- ✅ Use `select_related()` para ForeignKey
- ✅ Use `prefetch_related()` para ManyToMany
- ✅ Filtre no QuerySet, não em Python

### 4. Organização
- ✅ Um app por funcionalidade
- ✅ Models em `models.py`, Views em `views.py`
- ✅ Templates organizados por app
- ✅ Use `related_name` em ForeignKeys

---

## 🔄 Comparação: Service vs Appointment

| Aspecto | Service (Simples) | Appointment (Complexo) |
|---------|------------------|------------------------|
| **Campos** | Campos básicos apenas | Campos + ForeignKeys |
| **Validação** | Validação automática do Django | `clean()` customizado com lógica de negócio |
| **Relacionamentos** | Nenhum | 2 ForeignKeys (User, Service) |
| **Formulário** | Usa todos os campos | Oculta campos (customer calculado automaticamente) |
| **View** | CRUD padrão | CreateView com `form_valid()` customizado |
| **Template** | Template padrão | Template com widgets específicos |

---

## 📚 Recursos Adicionais

- **Django Documentation**: https://docs.djangoproject.com/
- **Class-Based Views**: https://ccbv.co.uk/
- **Django Girls Tutorial**: https://tutorial.djangogirls.org/
- **Two Scoops of Django**: Livro de boas práticas

---

## 🎓 Exercícios Propostos

1. **Criar Model de Cliente (Customer)**
   - Estender User com perfil
   - Adicionar telefone, endereço
   - Relacionar com Appointment

2. **Adicionar Status ao Appointment**
   - Implementar workflow (pending → confirmed → completed)
   - Adicionar view para mudar status
   - Validar transições de status

3. **Dashboard com Métricas**
   - Contar appointments por status
   - Calcular receita do mês
   - Mostrar próximos agendamentos

4. **Sistema de Notificações**
   - Email ao criar agendamento
   - Lembrete 1 dia antes
   - Usar Django signals

5. **Login automático (extra)**
    - Entrar com uma conta google
    - Entrar com uma conta apple
---

**Desenvolvido como material de estudo - Plataforma de Agendamentos**
*Última atualização: Fevereiro 2026*
