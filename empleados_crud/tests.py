from django.test import TestCase
from django.urls import reverse

from .models import CustomUser

class RegistroUsuarioTests(TestCase):
    def test_muestra_el_formulario_de_registro(self):
        response = self.client.get(reverse('registrarse'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crear cuenta')

    def test_registro_crea_usuario_con_rol_seguro(self):
        response = self.client.post(reverse('registrarse'), {
            'username': 'nueva.ingeniera',
            'first_name': 'Ana',
            'last_name': 'Pérez',
            'email': 'ana@example.com',
            'cedula': '123456789',
            'telefono': '3001234567',
            'password1': 'Una-clave-segura-2026',
            'password2': 'Una-clave-segura-2026',
        })

        self.assertRedirects(response, reverse('iniciarSesion'))
        user = CustomUser.objects.get(username='nueva.ingeniera')
        self.assertEqual(user.rol, 'Ingeniero civil')
        self.assertTrue(user.check_password('Una-clave-segura-2026'))
