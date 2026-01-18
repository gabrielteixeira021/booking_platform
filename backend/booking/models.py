from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(_(""))
    price = models.DecimalField(_(""), max_digits=8, decimal_places=2)
    is_active = models.BooleanField(_(""), default=True)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("confirmed", "confirmado"),
        ("cancelled", "Cancelado"),
    ]
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Cliente"), on_delete=models.CASCADE, related_name="appointments")
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments")

    start_time = models.DateTimeField(_("início do serviço"), auto_now=False, auto_now_add=False) 
    end_time = models.DateTimeField(_("término do serviço"), auto_now=False, auto_now_add=False)
    status = models.CharField(_("status"), max_length=10, choices=STATUS_CHOICES, default="pending")
    
    created_at = models.DateTimeField(_("data de criação do serviço"), auto_now=False, auto_now_add=True)
    
    class Meta:
        ordering = ["-start_time"]
        
    def __str__(self):
        return f"{self.customer} - {self.service} em {self.start_time}"
    