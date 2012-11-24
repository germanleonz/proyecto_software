from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
import re

def validate_user(value):
	if re.match('^[a-zA-Z]+[a-zA-Z-_.0-9]+$',value)==None:
		raise ValidationError(u'\"%s\"no es un usuario valido' % value)

def validate_nombre(value):
	if re.match('^[a-zA-Z]+$',value)==None:
		raise ValidationError(u'\"%s\" no es un nombre valido, debe estar compuesto solo por letras.' % value)

def validate_apellido(value):
	if re.match('^[a-zA-Z]+$',value)==None:
		raise ValidationError(u'\"%s\" no es un apellido valido, debe estar compuesto solo por letras' % value)

def validate_telefono(value):
   	if re.match('^[0-9]+[-]?[0-9]+$', value) == None:
		raise ValidationError(u'\"%s\" no es un telefono valido' % value)

def validate_password(value):
	if len(value)<6:
		raise ValidationError(u' Clave Invalida')
	      
def validate_unico(value):
	if not User.objects.filter(username = value):
		pass
	else:
		raise ValidationError(u'Ya existe usuario con ese Nombre')





class LoginForm (forms.Form):    

    class Meta:
            model = User

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['nombre_usuario'].error_messages = {'required': 'El nombre de usuario es obligatorio'}
        self.fields['password'].error_messages = {'required': 'La clave es obligatoria'}

    """
    Form para registrarse en el sistema
    """	
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
    """
    nuevo_nombre_usuario = forms.CharField(max_length=30, validators=[validate_unico,validate_user])	
    nueva_password = forms.CharField(widget=forms.PasswordInput, max_length=15,validators=[validate_password])
    nuevo_correo = forms.EmailField(max_length=50, error_messages={'invalid': ('La direccion de correo es invalida')})
    nuevo_nombre = forms.CharField(max_length=80,validators=[validate_nombre])
    nuevo_apellido = forms.CharField(max_length=20,validators=[validate_apellido])
    nuevo_telefono = forms.CharField(max_length=15,validators=[validate_telefono])

class ModificarUsuarioForm(forms.Form):
    """
    Form para modificar un usuario que ya este registrado en el sistema
    """
    nombre = forms.CharField(max_length=80,validators=[validate_nombre])
    apellido = forms.CharField(max_length=20,validators=[validate_apellido])
    telefono = forms.CharField(max_length=15,validators=[validate_telefono])
    correo = forms.EmailField(max_length=50, error_messages={'invalid': ('La direccion de correo es invalida')})
