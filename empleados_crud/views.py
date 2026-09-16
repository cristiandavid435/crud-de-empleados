from django.shortcuts import render,redirect #Llamamos desde django.shortcuts render y redirect
from django.contrib.auth.forms import AuthenticationForm  #Llamamos desde django.contrib.auth.forms AuthenticationForm
from django.contrib.auth import authenticate, login , logout #importamos desde django.contrib.auth  authenticate, login , logout
from .forms import PrestamoHerramientaForm,NominaForm,CustomUserCreationForm,CustomUserEditForm,RegistroUsuarioForm #Llamamos desde forms estos formulario
from .models import PrestamoHerramienta,Nomina,CustomUser # Importar los modelos
from .decorators import admin_required, admin_or_ingeniero
from django.contrib.auth.decorators import login_required



#Función que muestra el inicio de la aplicación
def index(request):
    return render(request,"index.html")

#funcion que autentica el usuario y contraseña que digite el cliente desde 
# el frontend 

#Si el metodo es get retornamos la misma página 
#SiNo (POST) autentica y envía los datos
def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request,'iniciarSesion.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'iniciarSesion.html',{
            'form': AuthenticationForm,
            'error':'Usuario o Contraseña incorrecta intente nuevamente!'
        })
        
        elif hasattr(user, "rol") and user.rol == "Maestro de obra":
            return render(request,'iniciarSesion.html',{
                'form': AuthenticationForm,
                'error': 'No tienes acceso al sistema'
            })
        else:
            login(request,user)
            return redirect('herramientas')


def registrarse(request):
    """Crea una cuenta pública con permisos de Ingeniero civil."""
    if request.user.is_authenticated:
        return redirect('herramientas')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('iniciarSesion')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registrarse.html', {'form': form})
        
@login_required     
@admin_required   
def crear_usuarios(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print("Datos recibidos:" , request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("lista_usuarios")
    else:
        form = CustomUserCreationForm()
        print("Errores del formulario:",  form.errors)
    return render (request,"crear_usuarios.html", {"form":form})

@login_required  
@admin_required
def lista_usuarios(request):
    if request.method == 'GET':
        usuarios_list = CustomUser.objects.all()
    else:
        usuarios_list = CustomUser.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios_list})

@login_required  
@admin_required
def editar_usuario(request, id):
    usuario = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        form = CustomUserEditForm(instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = CustomUserCreationForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario':usuario})

@login_required  
@admin_or_ingeniero
#Funcion que registra herramientas
def herramientas(request):
    #Si el metodo es POST guardamos el formulario de las herramientas en la variable form y validamos
    # si el formulario es valido guardamos y volvemos al formulario(En este caso vamos a ir a la lista de herramientas)
    #Si el método no es POST entonces no envía nada
    if request.method == 'POST':
        form = PrestamoHerramientaForm(request.POST)
        if form.is_valid():
            # Guardar el modelo
            herramienta = form.save(commit=False)
            herramienta.registrado_por = request.user
            herramienta.save()
            return redirect('lista_herramientas')
    else:
        form = PrestamoHerramientaForm()
    
    # Obtener todas las herramientas registradas
    
    return render(request, 'Herramienta.html', {'form': form})

@login_required
@admin_or_ingeniero
def editar_herramienta(request, id):
    herramienta = PrestamoHerramienta.objects.get(id=id)

    if request.method == 'POST':
        form = PrestamoHerramientaForm(request.POST, instance=herramienta)
        if form.is_valid():
            herramienta_edit = form.save(commit=False)
            
            herramienta_edit.registrado_por = request.user

            herramienta_edit.save()
            return redirect('lista_herramientas')

    else:
        form = PrestamoHerramientaForm(instance=herramienta)

    return render(request, 'editar_herramienta.html', {
        'form': form,
        'herramienta': herramienta
    })



@login_required  
@admin_or_ingeniero   
def eliminar_herramienta(request,id):
    herramienta = PrestamoHerramienta.objects.get(id=id)
    if request.method == 'POST':
        herramienta.delete()
        return redirect('lista_herramientas')
    else:
        return render(request, 'confirmar_eliminar_herramienta.html', {'herramienta': herramienta})

#El administrador tiene acceso a todos los datos tanto a los que el registra como a los que registran sus ingenieros
@login_required
@admin_or_ingeniero
def lista_herramientas(request):

    # 🔹 1. Query base (SIEMPRE se define)
    if request.user.rol == 'Administrador':
        herramientas = PrestamoHerramienta.objects.all()
    else:
        herramientas = PrestamoHerramienta.objects.filter(
            registrado_por=request.user
        )

    # 🔹 2. Filtro por fechas
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        herramientas = herramientas.filter(
            fecha_entrega__range=[fecha_inicio, fecha_fin]
        )

    return render(request, 'lista_de_herramientas.html', {
        'herramientas': herramientas
    })


@login_required  
@admin_or_ingeniero
def nomina(request):
    if request.method == 'POST':
        form = NominaForm(request.POST)
        if form.is_valid():
            nomina = form.save(commit=False)
            nomina.registrado_por = request.user
            # Calculo automático
            nomina.total_pagar = (
                nomina.salario_base * nomina.horas_trabajadas
            ) + nomina.bonificaciones - nomina.descuentos

            nomina.save()
            return redirect('empleados_nomina')
    else:
        form = NominaForm()

    return render(request, 'nomina.html', {'form': form})


#El administrador tiene acceso a todos los datos tanto a los que el registra como a los que registran sus ingenieros
@login_required  
@admin_or_ingeniero
def empleados_nomina(request):
    if request.user.rol =='Administrador':
        nomina_list = Nomina.objects.all()
    else:
        nomina_list = Nomina.objects.filter(registrado_por = request.user)
        
    fecha_inicio = request.GET.get('fecha_inicio')
    
    if fecha_inicio:
        nomina_list = nomina_list.filter(fecha_pago=fecha_inicio)
    return render(request,'empleados_nomina.html', {'nominas':nomina_list})

@login_required
@admin_or_ingeniero
def editar_nomina(request, id):
    nomina = Nomina.objects.get(id=id)

    if request.method == 'POST':
        form = NominaForm(request.POST, instance=nomina)

        if form.is_valid():
            nomina_edit = form.save(commit=False)
            nomina_edit.registrado_por = request.user
            nomina_edit.save()
            return redirect('empleados_nomina')

    else:
        form = NominaForm(instance=nomina)

    return render(request, 'editar_nomina.html', {
        'form': form,
        'nomina': nomina
    })

from django.http import HttpResponse
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime

from django.shortcuts import render,redirect #Llamamos desde django.shortcuts render y redirect
from django.contrib.auth.forms import AuthenticationForm  #Llamamos desde django.contrib.auth.forms AuthenticationForm
from django.contrib.auth import authenticate, login , logout #importamos desde django.contrib.auth  authenticate, login , logout
from django.contrib.auth.models import User #importamos desde django contrib . auth models el modelo de usuarios (User)
from .forms import PrestamoHerramientaForm,NominaForm,CustomUserCreationForm,CustomUserEditForm #Llamamos desde forms estos formulario
from .models import PrestamoHerramienta,Nomina,CustomUser # Importar los modelos
from .decorators import admin_required, admin_or_ingeniero
from django.contrib.auth.decorators import login_required



#Función que muestra el inicio de la aplicación
def index(request):
    return render(request,"index.html")

#funcion que autentica el usuario y contraseña que digite el cliente desde 
# el frontend 

#Si el metodo es get retornamos la misma página 
#SiNo (POST) autentica y envía los datos
def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request,'iniciarSesion.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'iniciarSesion.html',{
            'form': AuthenticationForm,
            'error':'Usuario o Contraseña incorrecta intente nuevamente!'
        })
        
        elif hasattr(user, "rol") and user.rol == "Maestro de obra":
            return render(request,'iniciarSesion.html',{
                'form': AuthenticationForm,
                'error': 'No tienes acceso al sistema'
            })
        else:
            login(request,user)
            return redirect('herramientas')
        
@login_required     
@admin_required   
def crear_usuarios(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print("Datos recibidos:" , request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("lista_usuarios")
    else:
        form = CustomUserCreationForm()
        print("Errores del formulario:",  form.errors)
    return render (request,"crear_usuarios.html", {"form":form})

@login_required  
@admin_required
def lista_usuarios(request):
    if request.method == 'GET':
        usuarios_list = CustomUser.objects.all()
    else:
        usuarios_list = CustomUser.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios_list})

@login_required  
@admin_required
def editar_usuario(request, id):
    usuario = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST,instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = CustomUserCreationForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario':usuario})

@login_required  
@admin_or_ingeniero
#Funcion que registra herramientas
def herramientas(request):
    #Si el metodo es POST guardamos el formulario de las herramientas en la variable form y validamos
    # si el formulario es valido guardamos y volvemos al formulario(En este caso vamos a ir a la lista de herramientas)
    #Si el método no es POST entonces no envía nada
    if request.method == 'POST':
        form = PrestamoHerramientaForm(request.POST)
        if form.is_valid():
            # Guardar el modelo
            herramienta = form.save(commit=False)
            herramienta.registrado_por = request.user
            herramienta.save()
            return redirect('lista_herramientas')
    else:
        form = PrestamoHerramientaForm()
    
    # Obtener todas las herramientas registradas
    
    return render(request, 'Herramienta.html', {'form': form})

@login_required
@admin_or_ingeniero
def editar_herramienta(request, id):
    herramienta = PrestamoHerramienta.objects.get(id=id)

    if request.method == 'POST':
        form = PrestamoHerramientaForm(request.POST, instance=herramienta)
        if form.is_valid():
            herramienta_edit = form.save(commit=False)
            
            herramienta_edit.registrado_por = request.user

            herramienta_edit.save()
            return redirect('lista_herramientas')

    else:
        form = PrestamoHerramientaForm(instance=herramienta)

    return render(request, 'editar_herramienta.html', {
        'form': form,
        'herramienta': herramienta
    })



@login_required  
@admin_or_ingeniero   
def eliminar_herramienta(request,id):
    herramienta = PrestamoHerramienta.objects.get(id=id)
    if request.method == 'POST':
        herramienta.delete()
        return redirect('lista_herramientas')
    else:
        return render(request, 'confirmar_eliminar_herramienta.html', {'herramienta': herramienta})

#El administrador tiene acceso a todos los datos tanto a los que el registra como a los que registran sus ingenieros
@login_required
@admin_or_ingeniero
def lista_herramientas(request):

    # 🔹 1. Query base (SIEMPRE se define)
    if request.user.rol == 'Administrador':
        herramientas = PrestamoHerramienta.objects.all()
    else:
        herramientas = PrestamoHerramienta.objects.filter(
            registrado_por=request.user
        )

    # 🔹 2. Filtro por fechas
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        herramientas = herramientas.filter(
            fecha_entrega__range=[fecha_inicio, fecha_fin]
        )

    return render(request, 'lista_de_herramientas.html', {
        'herramientas': herramientas
    })


@login_required  
@admin_or_ingeniero
def nomina(request):
    if request.method == 'POST':
        form = NominaForm(request.POST)
        if form.is_valid():
            nomina = form.save(commit=False)
            nomina.registrado_por = request.user
            # Calculo automático
            nomina.total_pagar = (
                nomina.salario_base * nomina.horas_trabajadas
            ) + nomina.bonificaciones - nomina.descuentos

            nomina.save()
            return redirect('empleados_nomina')
    else:
        form = NominaForm()

    return render(request, 'nomina.html', {'form': form})


#El administrador tiene acceso a todos los datos tanto a los que el registra como a los que registran sus ingenieros
@login_required  
@admin_or_ingeniero
def empleados_nomina(request):
    if request.user.rol =='Administrador':
        nomina_list = Nomina.objects.all()
    else:
        nomina_list = Nomina.objects.filter(registrado_por = request.user)
    
    # 🔹 CORREGIDO: Filtro por rango de fechas
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if fecha_inicio and fecha_fin:
        nomina_list = nomina_list.filter(fecha_pago__range=[fecha_inicio, fecha_fin])
    
    return render(request,'empleados_nomina.html', {'nominas':nomina_list})

@login_required
@admin_or_ingeniero
def editar_nomina(request, id):
    nomina = Nomina.objects.get(id=id)

    if request.method == 'POST':
        form = NominaForm(request.POST, instance=nomina)

        if form.is_valid():
            nomina_edit = form.save(commit=False)
            nomina_edit.registrado_por = request.user
            nomina_edit.save()
            return redirect('empleados_nomina')

    else:
        form = NominaForm(instance=nomina)

    return render(request, 'editar_nomina.html', {
        'form': form,
        'nomina': nomina
    })

from django.http import HttpResponse
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime

@login_required
@admin_or_ingeniero
def exportar_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active

    # 🔹 Estilos reutilizables
    header_fill = PatternFill(start_color="0088EE", end_color="0088EE", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")

    tipo = request.GET.get('tipo', 'herramientas')

    # =====================================================
    # 🔧 EXPORTAR HERRAMIENTAS
    # =====================================================
    if tipo == 'herramientas':
        ws.title = "Herramientas"

        encabezados = [
            'Nombre', 'Tipo', 'Cantidad', 'Empleado Asignado',
            'Registrado por', 'Fecha Entrega', 'Fecha Devolución',
            'Estado', 'Observaciones'
        ]

        for col_num, encabezado in enumerate(encabezados, 1):
            cell = ws.cell(row=1, column=col_num, value=encabezado)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")

        if request.user.rol == 'Administrador':
            data = PrestamoHerramienta.objects.all()
        else:
            data = PrestamoHerramienta.objects.filter(registrado_por=request.user)

        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            data = data.filter(fecha_entrega__range=[fecha_inicio, fecha_fin])

        for row_num, h in enumerate(data, 2):
            ws.cell(row=row_num, column=1).value = h.nombre_herramienta
            ws.cell(row=row_num, column=2).value = h.tipo
            ws.cell(row=row_num, column=3).value = h.cantidad
            ws.cell(row=row_num, column=4).value = f"{h.empleado_asignado.first_name} {h.empleado_asignado.last_name}"
            ws.cell(row=row_num, column=5).value = f"{h.registrado_por.first_name} {h.registrado_por.last_name}"
            ws.cell(row=row_num, column=6).value = h.fecha_entrega
            ws.cell(row=row_num, column=7).value = h.fecha_devolucion or "Pendiente"
            ws.cell(row=row_num, column=8).value = h.get_estado_display()
            ws.cell(row=row_num, column=9).value = h.observaciones or "N/A"

        filename = "herramientas"

    # =====================================================
    # 💰 EXPORTAR NÓMINA
    # =====================================================
    elif tipo == 'nomina':
        ws.title = "Nomina"

        encabezados = [
            'Empleado', 'Salario Base', 'Horas',
            'Bonificaciones', 'Descuentos',
            'Total a Pagar', 'Fecha Pago',
            'Estado', 'Observaciones', 'Registrado por'
        ]

        for col_num, encabezado in enumerate(encabezados, 1):
            cell = ws.cell(row=1, column=col_num, value=encabezado)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")

        if request.user.rol == 'Administrador':
            data = Nomina.objects.all()
        else:
            data = Nomina.objects.filter(registrado_por=request.user)

        # 🔹 CORREGIDO: Usar rango de fechas como en herramientas
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            data = data.filter(fecha_pago__range=[fecha_inicio, fecha_fin])

        for row_num, n in enumerate(data, 2):
            ws.cell(row=row_num, column=1).value = f"{n.empleado.first_name} {n.empleado.last_name}"
            ws.cell(row=row_num, column=2).value = n.salario_base
            ws.cell(row=row_num, column=3).value = n.horas_trabajadas
            ws.cell(row=row_num, column=4).value = n.bonificaciones
            ws.cell(row=row_num, column=5).value = n.descuentos
            ws.cell(row=row_num, column=6).value = n.total_pagar
            ws.cell(row=row_num, column=7).value = n.fecha_pago
            ws.cell(row=row_num, column=8).value = n.estado_pago
            ws.cell(row=row_num, column=9).value = n.observaciones
            ws.cell(row=row_num, column=10).value = f"{n.registrado_por.first_name} {n.registrado_por.last_name}"

        filename = "nomina"

    for column in ws.columns:
        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in column)
        ws.column_dimensions[column[0].column_letter].width = max_length + 2

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = (
        f'attachment; filename={filename}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    )

    wb.save(response)
    return response



def cerrarSesion(request):
    logout(request)
    return redirect('index')



def cerrarSesion(request):
    logout(request)
    return redirect('index')

