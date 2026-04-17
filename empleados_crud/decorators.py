from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    """
    Solo permite acceso a Administradores.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')

        if not hasattr(request.user, "rol") or request.user.rol != 'Administrador':
            return redirect('index')

        return view_func(request, *args, **kwargs)

    return wrapper


def admin_or_ingeniero(view_func):
    """
    Permite acceso a Administradores e Ingenieros Civiles.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')

        if not hasattr(request.user, "rol"):
            return redirect('index')

        if request.user.rol not in ['Administrador', 'Ingeniero civil']:
            return redirect('index')

        return view_func(request, *args, **kwargs)

    return wrapper
