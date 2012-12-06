from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string

from app_usuarios.forms import CrearUsuarioForm, CambiarContrasenaForm

@dajaxice_register
def crearUsuarioAjax(request):
	form = CrearUsuarioForm()
	vista = render_to_string('app_usuarios/crear_usuario.html',{'form':form})
	return simplejson.dumps({'vista': vista})

@dajaxice_register
def cambiarContrasenaAjax(request):
	form = CambiarContrasenaForm()
	vista = render_to_string('app_usuarios/cambiar_contrasena.html', {'form':form})
	return simplejson.dumps({'vista': vista})
