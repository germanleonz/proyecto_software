#coding=utf-8
"""
Pruebas funcionales del sistema. Utilizando las herramientas
TDD Selenium, Mock, etc
"""

from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from django.test.client import Client

from app_usuarios.models import UserProfile

class PizarraTestCase(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

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
        self.assertEquals(len(pizarras_links), 1)

        #   Hacemos click en el link sobre las pizarras
        pizarras_links[0].click()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 pizarras', body.text)

        new_pizarra_link = self.browser.find_element_by_link_text('Add pizarra')
        new_pizarra_link.click()

        #   Ve unos campos de input para los distintos campos de una pizarra   
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Nombrepiz:', body.text)
        self.assertIn('Descripcionpiz:', body.text)
        self.assertIn('Fechacreacion:', body.text)
        self.assertIn('Fechafinal:', body.text)
        self.assertIn('Avancepiz:', body.text)
        self.assertIn('Logindueno:', body.text)

        #   Agregamos los valores para los distintos campos de la pizarra
        nombre_field = self.browser.find_element_by_name('nombrepiz')
        nombre_field.send_keys("Nombre de la pizarra de prueba")
        descripcion_field = self.browser.find_element_by_name('descripcionpiz')
        descripcion_field.send_keys("Descripcion de la pizarra de prueba")

        now = date.today()
        fechainicio_field = self.browser.find_element_by_name('fechacreacion')
        fechainicio_field.send_keys(now.strftime("%d/%m/%Y"))
        fechafin_field = self.browser.find_element_by_name('fechafinal')
        fechafin_field.send_keys(now.replace(day=now.day+1).strftime("%d/%m/%Y"))
        avance_field = self.browser.find_element_by_name('avancepiz')
        avance_field.send_keys("0")

        select = Select(self.browser.find_element_by_tag_name("select"))
        select.select_by_visible_text("admin")

        #   Hacemos click al boton de save
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()

        #   Volvemos al listado de las pizarras, donde podemos ver el nombre
        #   de la pizarra que acabamos de crear  
        nuevos_links_de_pizarras = self.browser.find_elements_by_link_text(
                "Nombre de la pizarra de prueba",
        )
        self.assertEquals(len(nuevos_links_de_pizarras), 1)

    def test_agregar_una_actividad_a_una_pizarra_ya_existente_desde_el_sitio_admin(self):
        """docstring for test_agregar_una_actividad_a_una_pizarra_ya_existente_desde_el_sitio_admin"""
        pass


class UserProfileTestCase(LiveServerTestCase):
    """docstring for UserProfileTestCase"""

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def test_user_can_register_and_login(self):
        """docstring for test_user_can_register_and_login"""
        self.browser.get(self.live_server_url)

        boton_registrarse = self.browser.find_element_by_id('nombre')
        self.assertIn('Registrarse', boton_registrarse.text)

        boton_registrarse.click()

        #   Debe aparecer el boton de registro ademas del formulario de registro
        form_registro = self.browser.find_element_by_id('loginForm')

        username_field = self.browser.find_element_by_name('nuevo_nombre_usuario')
        username_field.send_keys('cronos')
        password_field = self.browser.find_element_by_name('nueva_password')
        password_field.send_keys('w2p1N5i7#')
        correo_field = self.browser.find_element_by_name('nuevo_correo')
        correo_field.send_keys('08-10611@ldc.usb.ve')
        first_name_field = self.browser.find_element_by_name('nuevo_nombre')
        first_name_field.send_keys('Cro')
        apellido_field = self.browser.find_element_by_name('nuevo_apellido')
        apellido_field.send_keys('Nos')
        telefono_field = self.browser.find_element_by_name('nuevo_telefono')
        telefono_field.send_keys('0424-1997501')

        #   El nuevo usuario se registra en el sistema
        boton_efectuar_registro = self.browser.find_element_by_css_selector("input[value='Registrarse']")
        boton_efectuar_registro.click()

        #   Una vez hecho el registro buscamos el formulario de login 
        #   para introducir las credenciales del usuario 
        username_login_field = self.browser.find_element_by_id('id_nombre_usuario')
        username_login_field.send_keys('cronos')
        password_login_field = self.browser.find_element_by_id('id_password')
        password_login_field.send_keys('w2p1N5i7#')

        #   El nuevo usuario entra al sistema
        boton_efectuar_registro = self.browser.find_element_by_css_selector("input[value='Iniciar Sesión']")
        boton_efectuar_registro.click()

        #   Verificamos que aparezca el nombre del usuario en la barra superior derecha   
        nombre_object = self.browser.find_element_by_id('nombre')
        self.assertIn('Cro Nos', nombre_object.text)

        self.fail('TODO')

    #def test_crear_un_nuevo_userprofile_desde_el_sitio_admin(self):
        #"""docstring for test_crear_un_nuevo_userprofile_desde_el_sitio_admin"""
        #self.browser.get(self.live_server_url)

        #username_field = self.browser.find_element_by_name('username')
        #username_field.send_keys('admin')

        #password_field = self.browser.find_element_by_name('password')
        #password_field.send_keys('django')
        #password_field.send_keys(Keys.RETURN)

        #datos_usuario = self.browser.find_element_by_id('nombre')
        ##nombre = self.assertIn(datos_usuario.text , "%s" % u.nombre)
        ##apellido = self.assertIn(datos_usuario.text , "%s" % u.apellido)

        ##   Creamos la pizarra

