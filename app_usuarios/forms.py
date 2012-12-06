from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
import re

def validate_user(value):
	"""
	Metodo para validar el username. Expresion regular a cumplir: '^[a-zA-Z]+[a-zA-Z-_.0-9]+$'
	In: value
	Autor: Mary Ontiveros
	Fecha: 8-11-12 Version 1.0
	"""
	if re.match('^[a-zA-Z]+[a-zA-Z-_.0-9]+$',value)==None:
		raise ValidationError(u'\"%s\"no es un usuario valido' % value)

def validate_nombre(value):
	"""
	Metodo para validar el nombre del usuario. Expresion regular a cumplir: '^[a-zA-Z]+$'
	In: value
	Autor: Mary Ontiveros
	Fecha: 8-11-12 Version 1.0
	"""
	if re.match('^[a-zA-Z]+$',value)==None:
		raise ValidationError(u'\"%s\" no es un nombre valido, debe estar compuesto solo por letras.' % value)

def validate_apellido(value):
	"""
	Metodo para validar el apellido de un usuario. Expresion regular: '^[a-zA-Z]+$'
	In: value
	Autor: Mary Ontiveros
	Fecha: 8-11-12 Version 1.0
	"""
	if re.match('^[a-zA-Z]+$',value)==None:
		raise ValidationError(u'\"%s\" no es un apellido valido, debe estar compuesto solo por letras' % value)

def validate_telefono(value):
	"""
	Metodo para validar el telefono de un usuario. Expresion regular: '^[0-9]+[-]?[0-9]+$'
	In: value
	Autor: Mary Ontiveros
	Fecha: 8-11-12 Version 1.0
	"""
	if re.match('^[0-9]+[-]?[0-9]+$', value) == None:
		raise ValidationError(u'\"%s\" no es un telefono valido' % value)

def validate_password(value):
	"""
	Metodo para validar la contrasena de un usuario. 
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
                raise ValidationError(u'Error en el nombre de usuario o contrasena')
        return cleaned_data        

class CrearUsuarioForm(forms.Form):
    """
    Form para crear un nuevo usuario en el sistema
    In: forms.Form
    Autor: German Leon
    Fecha: 8-11-12 Version 1.0
    """
    nuevo_nombre_usuario = forms.CharField(label="Introduzca un nombre de usuario",max_length=30, validators=[validate_unico,validate_user])	
    nueva_password = forms.CharField(label="Introduzca una contrasena", widget=forms.PasswordInput, max_length=15,validators=[validate_password])
    nuevo_correo = forms.EmailField(label="Introduzca una direccion de correo electronico", max_length=50, error_messages={'invalid': ('La direccion de correo es invalida')})
    nuevo_nombre = forms.CharField(label="Introduzca un nombre", max_length=80,validators=[validate_nombre])
    nuevo_apellido = forms.CharField(label="Introduzca un apellido", max_length=20,validators=[validate_apellido])
    nuevo_telefono = forms.CharField(label="Introduzca un numero de telefono", max_length=15,validators=[validate_telefono])
    nuevo_administrador = forms.BooleanField(label="Administrador", initial=False)

class ModificarUsuarioForm(forms.Form):
    """
    Form para modificar un usuario que ya este registrado en el sistema
    In: forms.Form
    Autor: German Leon
    Fecha: 8-11-12 Version 1.0
    """
    nombre = forms.CharField(max_length=80,validators=[validate_nombre])
    apellido = forms.CharField(max_length=20,validators=[validate_apellido])
    telefono = forms.CharField(max_length=15,validators=[validate_telefono])
    correo = forms.EmailField(max_length=50, error_messages={'invalid': ('La direccion de correo es invalida')})

class CambiarContrasenaForm(forms.Form):
    """
    Form para cambiar la contrasena de un usuario
    In: forms.Form
    Autor: German Leon
    Fecha: 20-11-12 Version 1.0
    """
    contrasena1 = forms.CharField(label = "Nueva contrasena", widget=forms.PasswordInput, max_length=15,validators=[validate_password])
    contrasena2 = forms.CharField(label = "Repita su nueva contrasena", widget=forms.PasswordInput, max_length=15,validators=[validate_password])

