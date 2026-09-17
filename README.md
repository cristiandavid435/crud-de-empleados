# CRUD de Empleados

Sistema web para gestionar empleados, nómina y préstamos de herramientas, desarrollado con Django.

## Descripción

Este proyecto permite administrar usuarios, registrar pagos, controlar asignación de herramientas y mantener diferentes niveles de acceso según el rol del usuario. Está pensado como una aplicación interna para gestión operativa.

## Tecnologías

- Python
- Django
- SQLite
- HTML/CSS/JavaScript

## Funcionalidades principales

- Registro e inicio de sesión
- Roles de usuario: Administrador, Ingeniero civil y Maestro de obra
- CRUD de usuarios
- Gestión de herramientas y préstamos
- Registro de nómina y cálculo de pagos
- Filtros por fecha
- Exportación de reportes a Excel

## Instalación rápida

```bash
git clone <url-del-repositorio>
cd CRUD_DE_EMPLEADOS
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Luego abre:

http://127.0.0.1:8000/
```

## Estado

Proyecto funcional en desarrollo, pensado como demostración de habilidades en Django, autenticación, permisos y lógica de negocio para portafolio.
