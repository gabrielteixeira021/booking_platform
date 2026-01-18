from django.contrib import admin
from .models import Service, Appointment

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_minutes", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    
    
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("customer", "service", "start_time", "status")
    list_filter = ("status", "service", "start_time")
    search_fields = ("customer__username", "service__name")