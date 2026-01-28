from datetime import timedelta
from django.db import models
from django.conf import settings
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Service(models.Model):
    name = models.CharField(_("nome"),max_length=100)
    description = models.TextField(_("descrição"), blank=True)
    duration_minutes = models.PositiveIntegerField(_("duração (min)"))
    price = models.DecimalField(_("preço"), max_digits=8, decimal_places=2)
    is_active = models.BooleanField(_("está ativo"), default=True)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("confirmed", "confirmado"),
        ("cancelled", "Cancelado"),
    ]
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Cliente"), on_delete=models.CASCADE, related_name="appointments")
    
    service = models.ForeignKey(Service, verbose_name=_("Serviço"), on_delete=models.CASCADE, related_name="appointments")

    start_time = models.DateTimeField(_("início do serviço"), auto_now=False, auto_now_add=False) 
    end_time = models.DateTimeField(_("término do serviço"), auto_now=False, auto_now_add=False)
    status = models.CharField(_("status"), max_length=10, choices=STATUS_CHOICES, default="pending")
    
    created_at = models.DateTimeField(_("data de criação do serviço"), auto_now=False, auto_now_add=True)

    def clean(self):
        from django.utils import timezone
        if self.start_time and self.start_time < timezone.now():
            raise ValidationError("Não é possível agendar no passado")
        
        if self.end_time and self.end_time <= self.start_time:
            raise ValidationError("Horário final deve ser depoiis do inicial")

        # Valida se há confilto de horário
        qs = Appointment.objects.filter(service=self.service)
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        # condição de overlap(sobreposição): start < outro_end e end > outro_start | quando o tempo de um serviço coincide com o de outro
        overlap = qs.filter(
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exists()

        if overlap:
            raise ValidationError("Já existe um agendamento nesse horário")
        
        def save(self, *args, **kwargs):
            # calcula end_time automaticamente baseado na duração do serviço
            if self.service and self.start_time and not self.end_time:
                self.end_time = self.start_time + timedelta(
                    minutes=self.service.duration_minutes
                )
            super().save(*args, **kwargs)


    class Meta:
        ordering = ["-start_time"]
        
    def __str__(self):
        return f"{self.customer} - {self.service} em {self.start_time}"
    