#coding=utf-8

import re

from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User

def validate_user(value):
	"""
	Metodo para validar el username. Expresion regular a cumplir: '^[a-zA-Z]+[a-zA-Z-_.0-9]+$'
	In: value
	Autor: Mary Ontiveros
	Fecha: 8-11-12 Version 1.0
	"""
	if re.match('^[a-zA-Z\xe1\xe9\xed\xf3\xfa\xc9\xcd\xd3\xda\xc1\xd1\xf1]+[a-zA-Z-_.0-9\xe1\xe9\xed\xf3\xfa\xc9\xcd\xd3\xda\xc1\xd1\xf1]+$',value)==None:
		raise ValidationError(u'\"%s\"no es un usuario válido' % value)

def validate_nombre(value):
	"""
	Metodo para validar el nombre del usuario. Expresion regular a cumplir: '^[a-zA-Z]+$'
	In: value
	Autor: Mary Ontiveros
	Fecha: 8-11-12 Version 1.0
	"""
	if re.match('(^$|^[A-Za-z0-9\xe1\xe9\xed\xf3\xfa\xc9\xcd\xd3\xda\xc1\xd1\xf1\¿\!\¡\:\,\.\-\ç\ñáéíóú\(\)\"\'\äëïöüàèìòù\s]*$)',value)==None:
		raise ValidationError(u'\"%s\" no es un nombre válido, debe estar compuesto solo por letras.' % value)

def validate_apellido(value):
	"""
	Metodo para validar el apellido de un usuario. Expresion regular: '^[a-zA-Z]+$'
	In: value
	Autor: Mary Ontiveros
	Fecha: 8-11-12 Version 1.0
	"""
	if re.match('(^$|^[a-zA-Z\'\xe1\xe9\xed\xf3\xfa\xc9\xcd\xd3\xda\xc1\xd1\xf1]+$)',value)==None:
		raise ValidationError(u'\"%s\" no es un apellido válido, debe estar compuesto solo por letras' % value)

def validate_telefono(value):
	"""
	Metodo para validar el teléfono de un usuario. Expresion regular: '^[0-9]+[-]?[0-9]+$'
	In: value
	Autor: Mary Ontiveros
	Fecha: 8-11-12 Version 1.0
	"""
	if re.match('^[0-9]+[-]?[0-9]+$', value) == None:
		raise ValidationError(u'\"%s\" no es un teléfono válido' % value)

def validate_password(value):
	"""
	Metodo para validar la contraseña de un usuario. 
	In: value
	Autor: Mary Ontiveros
	Fecha: 8-11-12 Version 1.0
	"""
	if len(value)<6:
		raise ValidationError(u' Clave Invalida')
	      
def validate_unico(value):
	"""
	Metodo para validar que solo exista un usuario con ese username
	In: value
	Autor: Mary Ontiveros
	Fecha: 8-11-12 Version 1.0
	"""
	if not User.objects.filter(username = value):
		pass
	else:
		raise ValidationError(u'Ya existe usuario con ese Nombre')


class LoginForm (forms.Form):    
    """
    Form para registrarse en el sistema
    In: forms.Form
    Autor: German Leon
    Fecha: 5-11-12 Version 1.0
    """	

    class Meta:
            model = User

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['nombre_usuario'].error_messages = {'required': 'El nombre de usuario es obligatorio'}
        self.fields['password'].error_messages = {'required': 'La clave es obligatoria'}

    nombre_usuario = forms.CharField(max_length=30, validators=[validate_user])
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("nombre_usuario")
        password = cleaned_data.get("password")

        if username and password:
            usuario = authenticate(username=username, password=password)
            if usuario is None:
                raise ValidationError(u'Error en el nombre de usuario o contraseña')
        return cleaned_data        

class CrearUsuarioForm(forms.Form):
    """
    Form para crear un nuevo usuario en el sistema
    In: forms.Form
    Autor: German Leon
    Fecha: 8-11-12 Version 1.0
    """
    nuevo_nombre_usuario = forms.CharField(label="Nombre de usuario",max_length=30, validators=[validate_unico,validate_user])	
    nueva_password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, max_length=15,validators=[validate_password])
    nuevo_correo = forms.EmailField(label="Dirección de correo electrónico", max_length=50, error_messages={'invalid': ('La dirección de correo es inválida')})
    nuevo_nombre = forms.CharField(label="Nombre", max_length=80,validators=[validate_nombre])
    nuevo_apellido = forms.CharField(label="Apellido", max_length=20,validators=[validate_apellido])
    nuevo_telefono = forms.CharField(label="Número de teléfono", max_length=15,validators=[validate_telefono])
    nuevo_administrador = forms.BooleanField(label="Administrador", initial=False, required = False)

class RegistrarVisitanteForm(forms.Form):
    """
    Form para registrar un usuario desde afuera del sistema
    In: forms.Form
    Autor: German Leon
    Fecha: 28-2-13 Version 1.0
    """
    nuevo_nombre_usuario = forms.CharField(label="Nombre de usuario",max_length=30, validators=[validate_unico,validate_user])	
    nueva_password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, max_length=15,validators=[validate_password])
    nuevo_correo = forms.EmailField(label="Dirección de correo electrónico", max_length=50, error_messages={'invalid': ('La dirección de correo es invalida')})
    nuevo_nombre = forms.CharField(label="Nombre", max_length=80,validators=[validate_nombre])
    nuevo_apellido = forms.CharField(label="Apellido", max_length=20,validators=[validate_apellido])
    nuevo_telefono = forms.CharField(label="Número de teléfono", max_length=15,validators=[validate_telefono])

class ModificarUsuarioForm(forms.Form):
    """
    Form para modificar un usuario que ya este registrado en el sistema
    In: forms.Form
    Autor: German Leon
    Fecha: 8-11-12 Version 1.0
    """
    nombre = forms.CharField(max_length=80,validators=[validate_nombre], required=False)
    apellido = forms.CharField(max_length=20,validators=[validate_apellido], required=False)
    telefono = forms.CharField(max_length=15,validators=[validate_telefono])
    correo = forms.EmailField(max_length=50, error_messages={'invalid': ('La dirección de correo es inválida')})

class CambiarContrasenaForm(forms.Form):
    """
    Form para cambiar la contraseña de un usuario
    In: forms.Form
    Autor: German Leon
    Fecha: 20-11-12 Version 1.0
    """
    contrasena1 = forms.CharField(label = "Nueva contraseña", widget=forms.PasswordInput, max_length=15,validators=[validate_password])
    contrasena2 = forms.CharField(label = "Repita su nueva contraseña", widget=forms.PasswordInput, max_length=15,validators=[validate_password])
