#coding=utf-8
"""
TDD para la verificacion de modelos de la aplicacion de usuarios
User y UserProfile
"""

from django.test import LiveServerTestCase

from app_usuarios.models import UserProfile
from app_usuarios.forms import CrearUsuarioForm, RegistrarVisitanteForm, LoginForm

class UserProfileModelTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def test_login_form(self):
        """docstring for test_login_form"""
        login_form = LoginForm()
