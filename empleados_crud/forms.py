from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .models import PrestamoHerramienta, Nomina

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    cedula = forms.IntegerField(required=True)
    telefono = forms.CharField(required=True)
    rol = forms.ChoiceField(choices=[
        ('', '-- Seleccione un cargo --'),
        ('Administrador', 'Administrador'),
        ('Ingeniero civil', 'Ingeniero civil'),
        ('Maestro de obra', 'Maestro de obra'),
    ], required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=False)  # Cambiar a False o agregar el campo en el HTML
    
    class Meta:
        model = User 
        fields = [
            "username",
            "first_name",
            "last_name",
            "rol",
            "email",
            "cedula",
            "telefono",
            "password1",
            "password2"
        ]


User = get_user_model()
class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "rol",
            "email",
            "cedula",
            "telefono"
        ]


User = get_user_model()
class PrestamoHerramientaForm (forms.ModelForm):
    
    empleado_asignado = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=False,                       # cambiar a True si es obligatorio
        widget=forms.Select(attrs={'class': 'container-input'}),
        empty_label='-- Seleccione empleado --'
    )
    
    class Meta:
        model = PrestamoHerramienta
        fields= [
            'nombre_herramienta','tipo','cantidad','empleado_asignado',
            'fecha_entrega','fecha_devolucion','estado','observaciones']
        widgets = {
            'nombre_herramienta': forms.TextInput(attrs={'class':'container-input labels','placeholder':'Digite el nombre de herramienta','required':'required'}),
            'tipo': forms.TextInput(attrs={'class':'container-input', 'placeholder': 'Digite el tipo', 'required':'required'}),
            'cantidad': forms.NumberInput(attrs={'class':'container-input','placeholder':'Digite la cantidad', 'required':'required'}),
            'empleado_asignado': forms.Select(attrs={'class':'container-input', 'required':'required'}),
            'fecha_entrega' : forms.DateInput(
                format = '%Y-%m-%d',
                attrs={'class':'container-input date','type':'date'}
            ),
            'fecha_devolucion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class':'container-input date','type':'date'}
            ),
            'estado': forms.Select(attrs={'class':'container-input '}),
            'observaciones': forms.Textarea(attrs={
                'placeholder':'Observaciones',
                'class':'container-input date',
                'rows': 3,
                'style': 'resize: none; height: 120px;'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['fecha_entrega'].input_formats = ['%Y-%m-%d']
        self.fields['fecha_devolucion'].input_formats = ['%Y-%m-%d']

User = get_user_model()
class NominaForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=True,                       # cambiar a True si es obligatorio
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='-- Seleccione empleado --'
    )
    
    class Meta:
        model = Nomina
        fields = [
            'empleado','salario_base','horas_trabajadas','bonificaciones','descuentos','total_pagar','fecha_pago',
            'estado_pago','observaciones'
        ]
        widgets = {
            'empleado':forms.Select(attrs={'class':'container-input','required':'required'}),
            'salario_base':forms.NumberInput(attrs={'class':'container-input','placeholder':'Digite el valor por hora del trabajador','required':'required'}),
            'horas_trabajadas':forms.NumberInput(attrs={'class':'container-input','placeholder':'Digite las horas trabajadas por el trabajador','required':'required'}),
            'bonificaciones':forms.NumberInput(attrs={'class':'container-input','placeholder':'Digite las bonificaciones del trabajador','required':'required','min':'0'}),
            'descuentos':forms.NumberInput(attrs={'class':'container-input','placeholder':'Digite los descuentos del trabajador n','required':'required'}),
            'total_pagar':forms.NumberInput(attrs={'class':'container-input','required':'required','readonly':'readonly'}),
            'fecha_pago': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class':'container-input',
                    'required':'required',
                    'type':'date'
                }
            ),            
            'estado_pago':forms.Select(attrs={'class':'container-input','required':'required'}),
            'observaciones': forms.Textarea(attrs={
                'class':'container-input',
                'required':'required',
                'rows': 3,
                'style': 'resize: none; height: 120px;'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['fecha_pago'].input_formats = ['%Y-%m-%d']


class SetPasswordFormPersonalizado(SetPasswordForm):
    """Formulario personalizado para cambio de contraseña con estilos personalizados."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizamos los campos
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'container-input',
            'placeholder': 'Nueva contraseña',
            'required': 'required',
            'autocomplete': 'new-password'
        })
        self.fields['new_password1'].label = 'Nueva contraseña'
        self.fields['new_password1'].help_text = ''
        
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'container-input',
            'placeholder': 'Confirmar contraseña',
            'required': 'required',
            'autocomplete': 'new-password'
        })
        self.fields['new_password2'].label = 'Confirmar contraseña'
        self.fields['new_password2'].help_text = ''
    
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if password:
            from django.contrib.auth.password_validation import validate_password
            try:
                validate_password(password, self.user)
            except forms.ValidationError:
                raise
        return password