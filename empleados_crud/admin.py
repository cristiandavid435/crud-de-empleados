from django.contrib import admin
from .models import PrestamoHerramienta , Nomina, CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class PrestamoHerramientaAdmin(admin.ModelAdmin):
    list_display = ('nombre_herramienta','empleado_asignado','fecha_entrega','fecha_devolucion','estado') 
    search_fields = ('nombre_herramienta', 'empleado_asignado__username')
admin.site.register(PrestamoHerramienta,PrestamoHerramientaAdmin)

class NominaAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'salario_base', 'total_pagar', 'fecha_pago', 'estado_pago')
    search_fields = ('empleado__username',)
admin.site.register(Nomina,NominaAdmin)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('cedula', 'telefono','rol')
            
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('cedula','telefono','rol'),
        }),
    )

    list_display = ('username', 'first_name', 'last_name', 'email', 'cedula', 'telefono','rol','is_staff')