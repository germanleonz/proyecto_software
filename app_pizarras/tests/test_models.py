#coding=utf-8

from datetime import date
from faker import Factory

from django.contrib.auth.models import User
from django.test import TestCase

from app_pizarras.models import Pizarra, CreadorPizarra

class PizarraModelTest(TestCase):
    """docstring for PizarraModelTest"""
    fixtures = ['some_users.json']

    def test_crear_una_nueva_pizarra_y_guardarla_en_la_bd(self): 

        faker = Factory.create()

        nombrepiz      = faker.word()
        descripcionpiz = faker.sentence()
        now            = date.today()
        fechacreacion  = now
        fechafinal     = now.replace(day = now.day+1)
        logindueno     = User.objects.get(username = 'johndoe')
        avancepiz      = faker.randomInt(0,99)

        num_pizarras_old = len(Pizarra.objects.all())

        CreadorPizarra(
                nombrepiz      = nombrepiz,
                descripcionpiz = descripcionpiz,
                fechacreacion  = fechacreacion,
                fechafinal     = fechafinal,
                usuario        = logindueno
        )

        pizarras_new = Pizarra.objects.all()

        self.assertEquals(len(pizarras_new), num_pizarras_old + 1)

    def test_actualizar_info_de_pizarra_luego_de_creacion(self):
        pass

    def test_eliminar_pizarra(self):
        pass

    def test_agregar_una_actividad_a_una_pizarra_y_guardar(self):
        pass
