#coding=utf-8
"""
TDD para verificar el correcto funcionamiento de los modelos definidos
para la aplicacion app_usuarios
"""

from faker import Factory

from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase

from app_usuarios.models import UserProfile

class UserProfileModelTest(TestCase):

    @classmethod
    def setUpClass(self):
        """docstring for setUpClass"""
        #   Creamos los grupos  de colaboradores y administradores
        administradores = Group(name = "Administradores")
        colaboradores   = Group(name = "Colaboradores")

        administradores.save()
        colaboradores.save()

    def test_creando_un_userprofile_y_guardandolo_en_la_db(self):
        """docstring for test_creando_un_userprofile_y_guardandolo_en_la_db"""
        faker = Factory.create()

        #   Cargando la informacion de un usuario que ya este creado en el sistema
        #admin =  User.objects.get(username='germanleonz')
        admin = User(username='germanleonz')
        admin.save()

        #   Empezamos creando un UserProfile
        data = {}
        data['nuevo_nombre_usuario'] = faker.userName()
        data['nuevo_correo']         = faker.email()
        data['nueva_password']       = faker.firstName()
        data['nuevo_nombre']         = faker.firstName()
        data['nuevo_apellido']       = faker.lastName()
        data['nuevo_telefono']       = str(faker.randomInt(0,9999999))

        #   Revisar que el UserProfile se guardo en la base de datos
        up = UserProfile.objects.crear_colaborador(data, admin)

        #   Revisamos que podemos buscarlo en la bd
        todos_los_usuarios_registrados = UserProfile.objects.all()
        self.assertEquals(len(todos_los_usuarios_registrados), 1)
        unicoUsuarioEnLaBd = todos_los_usuarios_registrados[0]
        self.assertEquals(unicoUsuarioEnLaBd, up) 

        #   Revisamos que tenga los atributos que esperamos   
        self.assertEquals(unicoUsuarioEnLaBd.user.username, data['nuevo_nombre_usuario'])
        self.assertEquals(unicoUsuarioEnLaBd.user.email, data['nuevo_correo'])
        self.assertEquals(unicoUsuarioEnLaBd.user.first_name, data['nuevo_nombre'])
        self.assertEquals(unicoUsuarioEnLaBd.user.last_name, data['nuevo_apellido'])
        self.assertEquals(unicoUsuarioEnLaBd.telefono, data['nuevo_telefono'])

    #def test_creando_un_userprofile_con_un_usuario_anonimo(self):
        #pass
