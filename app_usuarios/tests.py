"""
Pruebas unitarias para el modulo encargado del manejo de usuarios 
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import UserProfile

class UsuarioTestCase(TestCase):
    def setUp(self):
        """docstring for setUp"""
        self.post_data = {
            'first_name' : 'German',
            'last_name' : 'Leon',
        }
        self.client = Client()

    def test_registro_ok(self):
        """
        Prueba que funcione correctamente el registro de usuarios
        """
        total_usuarios = User.objects.count()
        k = {'user_type': 'user'}
        response = self.client.post(reverse('registrar_visitante', kwargs=k), self.post_data);
        self.assertEquals(User.objects.count(), total_usuarios + 1)

