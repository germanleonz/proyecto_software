from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from app_usuarios.forms import CrearUsuarioForm, CambiarContrasenaForm
from app_usuarios.models import UserProfile

@dajaxice_register
def crearUsuarioAjax(request):
	form = CrearUsuarioForm()
	vista = render_to_string('app_usuarios/crear_usuario.html',{'form':form})
	return simplejson.dumps({'vista': vista})

@dajaxice_register
def modificarUsuarioAjax(request,nombre_usuario):
    lista = []
    usuario = User.objects.get(id=nombre_usuario)
    uname = usuario.username
    lista.append(usuario.first_name)
    lista.append(usuario.last_name)
    lista.append(usuario.email)
    perfil = UserProfile.objects.get(user = usuario)
    lista.append(perfil.telefono)
    vista = render_to_string('app_usuarios/modificar_usuario.html',{'lista':lista, 'nombre_usuario': uname})
    return simplejson.dumps({'vista': vista})

@dajaxice_register
def editarPerfilAjax(request):
    usuario = request.user
    nombre_usuario = usuario.username
    lista = []
    lista.append(usuario.first_name)
    lista.append(usuario.last_name)
    lista.append(usuario.email)
    perfil = UserProfile.objects.get(user = usuario)
    lista.append(perfil.telefono)
    vista = render_to_string('app_usuarios/modificar_usuario.html', {'lista':lista, 'nombre_usuario': nombre_usuario})
    return simplejson.dumps({'vista': vista})

@dajaxice_register
def cambiarContrasenaAjax(request):
	form = CambiarContrasenaForm()
	vista = render_to_string('app_usuarios/cambiar_contrasena.html', {'form':form})
	return simplejson.dumps({'vista': vista})
