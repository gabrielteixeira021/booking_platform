# 📅 Booking Platform

[![Django](https://img.shields.io/badge/Django-6.0.1-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Sistema profissional de agendamento de serviços desenvolvido com Django, oferecendo uma solução completa para gerenciamento de reservas e compromissos.

## 🎯 Sobre o Projeto

O **Booking Platform** é uma aplicação web robusta desenvolvida em Django que permite o gerenciamento eficiente de agendamentos de serviços. O sistema oferece funcionalidades completas para cadastro de serviços, controle de horários e gerenciamento de compromissos com diferentes status.

### ✨ Principais Funcionalidades

- **Gerenciamento de Serviços**: Cadastro completo de serviços com nome, descrição, duração e preço
- **Sistema de Agendamentos**: Controle total de compromissos com horário de início e término
- **Status de Agendamento**: Acompanhamento do status (Pendente, Confirmado, Cancelado)
- **Painel Administrativo**: Interface administrativa completa do Django
- **Autenticação de Usuários**: Sistema integrado de autenticação
- **Relacionamento Cliente-Serviço**: Vínculo entre clientes e serviços agendados

## 🏗️ Arquitetura

O projeto segue as melhores práticas do Django com uma arquitetura MVC (Model-View-Controller):

```
booking_platform/
├── backend/
│   ├── manage.py              # Gerenciador do Django
│   ├── requirements.txt       # Dependências do projeto
│   ├── db.sqlite3            # Banco de dados SQLite
│   ├── backend/              # Configurações principais
│   │   ├── settings.py       # Configurações do projeto
│   │   ├── urls.py          # Roteamento principal
│   │   └── wsgi.py          # Configuração WSGI
│   └── booking/             # App de agendamentos
│       ├── models.py        # Modelos de dados
│       ├── views.py         # Lógica de visualização
│       ├── admin.py         # Configuração do admin
│       └── migrations/      # Migrações do banco
```

## 🗄️ Modelo de Dados

### Service (Serviço)
- `name`: Nome do serviço
- `description`: Descrição detalhada
- `duration_minutes`: Duração em minutos
- `price`: Valor do serviço
- `is_active`: Status de disponibilidade

### Appointment (Agendamento)
- `customer`: Cliente vinculado (ForeignKey para User)
- `service`: Serviço contratado
- `start_time`: Horário de início
- `end_time`: Horário de término
- `status`: Status do agendamento (Pendente/Confirmado/Cancelado)
- `created_at`: Data de criação

## 🚀 Tecnologias Utilizadas

- **Backend Framework**: Django 6.0.1
- **Linguagem**: Python 3.8+
- **Banco de Dados**: SQLite (desenvolvimento)
- **Gerenciamento de Configurações**: Python-decouple
- **ORM**: Django ORM

## 💻 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/gabrielteixeira021/booking_platform.git
cd booking_platform
```

2. **Crie e ative o ambiente virtual**
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instale as dependências**
```bash
cd backend
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na pasta `backend/` com as seguintes variáveis:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=db.sqlite3
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

7. **Inicie o servidor de desenvolvimento**
```bash
python manage.py runserver
```

8. **Acesse a aplicação**
- Aplicação: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 🔧 Configuração

O projeto utiliza **python-decouple** para gerenciamento de configurações sensíveis. Todas as configurações importantes devem ser definidas no arquivo `.env`:

- `SECRET_KEY`: Chave secreta do Django
- `DEBUG`: Modo de depuração (True/False)
- `ALLOWED_HOSTS`: Hosts permitidos (separados por vírgula)
- `DB_NAME`: Nome do banco de dados

## 🧪 Testes

```bash
python manage.py test
```

## 📦 Deploy

Para preparar o projeto para produção:

1. Configure `DEBUG=False` no arquivo `.env`
2. Configure `ALLOWED_HOSTS` com seu domínio
3. Use um banco de dados robusto (PostgreSQL recomendado)
4. Configure arquivos estáticos com `collectstatic`
5. Use um servidor WSGI como Gunicorn ou uWSGI

## 🛠️ Desenvolvimento

### Estrutura de Código

- **Models**: Definição de entidades do banco de dados
- **Views**: Lógica de processamento de requisições
- **Admin**: Customização do painel administrativo
- **Migrations**: Controle de versão do banco de dados

### Boas Práticas Implementadas

✅ Uso de variáveis de ambiente para configurações sensíveis  
✅ Internacionalização com `gettext_lazy`  
✅ Relacionamentos adequados entre modelos  
✅ Ordenação padrão em querysets  
✅ Validação de dados com choices  
✅ Timestamps automáticos

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Gabriel Teixeira**

- GitHub: [@gabrielteixeira021](https://github.com/gabrielteixeira021)

## 📞 Contato

Para dúvidas ou sugestões, entre em contato através do GitHub.

---

Projeto desenvolvido para fins educativos.

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
