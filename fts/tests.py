"""
Pruebas unitarias para el modulo encargado del manejo de usuarios 
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from app_usuarios.models import UserProfile

class UsuarioTestCase(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_pizarra_via_admin_site(self):
        self.browser.get(self.live_server_url + '/admin/')

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('django')
        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        pizarras_links = self.browser.find_elements_by_link_text('Pizarras')
        self.assertEquals(len(pizarras_links), 2)

        self.fail('TODO')

class PizarraTestCase(LiveServerTestCase):
    """docstring for PizarraTestCase"""
    def test_crear_una_nueva_pizarra(self):
        """docstring for test_crear_una_nueva_pizarra"""
        self.browser.get(self.live_server_url)

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('germanleonz')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('123456')
        password_field.send_keys(Keys.RETURN)

        datos_usuario = self.browser.find_element_by_id('nombre')
        #nombre = self.assertIn(datos_usuario.text , "%s" % u.nombre)
        #apellido = self.assertIn(datos_usuario.text , "%s" % u.apellido)

