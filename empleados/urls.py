"""
URL configuration for empleados project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from empleados_crud import views
from django.contrib.auth import views as auth_views
from empleados_crud.forms import SetPasswordFormPersonalizado

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('iniciarSesion/', views.iniciar_sesion , name='iniciarSesion'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('herramientas/', views.herramientas ,name='herramientas'),
    path('lista_herramientas/', views.lista_herramientas, name='lista_herramientas'),
    path('nomina/',views.nomina, name='nomina'),
    path('editar_nomina/<int:id>/', views.editar_nomina, name='editar_nomina'),
    path('empleados_nomina/',views.empleados_nomina, name='empleados_nomina'),
    path('crear_usuarios/', views.crear_usuarios,name='crear_usuarios'),
    path('lista_usuarios/' , views.lista_usuarios, name='lista_usuarios'),
    path('editar_usuario<int:id>/' ,views.editar_usuario, name='editar_usuario'),
    path('cerrarSesion/', views.cerrarSesion ,name = 'cerrarSesion'),
    path('editar_herramienta/<int:id>/', views.editar_herramienta, name='editar_herramienta'),
    path('eliminar_herramienta/<int:id>/' ,views.eliminar_herramienta, name='eliminar_herramienta'),
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),

    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',
             form_class=SetPasswordFormPersonalizado
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    
    path('exportar_excel/' , views.exportar_excel, name='exportar_excel')
]

