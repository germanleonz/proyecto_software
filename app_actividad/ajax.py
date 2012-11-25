from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from app_actividad.forms import CrearActividadForm

@dajaxice_register
def crearActividadForm(request,data):
    form = CrearActividadForm()
    vista = render_to_string('app_actividad/crear_actividad.html',{'form':form, 'idpiz': data})
    return simplejson.dumps({'vista': vista})


@dajaxice_register
def mostrarActividad(request,data):
    vista = render_to_string('app_actividad/vistaActividad.html', {'actividad:': data})
    return simplejson.dumps({'vista': vista})
