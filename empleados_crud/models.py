from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError

#Gerente general(acceso al software)
#Ingeniero civil
#Maestro de obra


class CustomUser(AbstractUser):
    ROLES = [
        ('Administrador','Administrador'),
        ('Ingeniero civil', 'Ingeniero civil'),
        ('Maestro de obra','Maestro de obra'),
    ]
    cedula = models.CharField(max_length=15,unique=True)
    telefono = models.CharField(max_length=15)
    rol = models.CharField(max_length= 20, choices=ROLES ,blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    REQUIRED_FIELDS = ['cedula']

class PrestamoHerramienta(models.Model):
    ESTADO_ENTREGA = [
        ('buena', 'Buena'),
        ('Regular', 'Regular'),
        ('Mala', 'Mala'),
    ]

    nombre_herramienta = models.CharField(max_length = 100,null=True)
    tipo = models.CharField(max_length=200,null=True)
    cantidad = models.PositiveIntegerField(null=True)
    empleado_asignado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True, related_name='herramientas_asignadas')
    registrado_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True, related_name='registro_de_herramienta_creado')
    fecha_entrega = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_ENTREGA, default='buena')
    observaciones = models.TextField(max_length=500,blank =True, null=True)
    
    def __str__(self):
        return f"{self.nombre_herramienta} asignada a {self.empleado_asignado}"
    
    def clean(self):
        if self.fecha_devolucion and self.fecha_entrega > self.fecha_entrega:
            raise ValidationError(
                'La fecha de entrega no puede ser mayor que la fecha de devolución'
            )


class Nomina(models.Model):
    ESTADO_PAGO= [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    ]

    empleado= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='nominas',null=True)
    registrado_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,related_name='registrado_por',null=True)
    salario_base = models.IntegerField()
    horas_trabajadas = models.IntegerField()
    bonificaciones = models.IntegerField()
    descuentos = models.IntegerField()
    total_pagar = models.IntegerField(blank=True,null=True)
    fecha_pago = models.DateField()
    estado_pago = models.CharField(max_length=10, choices=ESTADO_PAGO, default='pendiente')
    observaciones = models.TextField(null=True,blank=True)
    
    
    class Meta:
        unique_together = ('empleado', 'fecha_pago')
    
    def __str__(self):
        return f"Nómina de {self.empleado.username} - {self.fecha_pago}"
    


    
