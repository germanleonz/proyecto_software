from app_usuarios.forms import CrearUsuarioForm

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string

@dajaxice_register
def crearUsuarioForm(request):
    form = CrearUsuarioForm()
    vista = render_to_string('app_usuarios/crear_usuario.html',{'form':form})
    return simplejson.dumps({'vista': vista})
