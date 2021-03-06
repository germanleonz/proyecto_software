from datetime import datetime
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.http import HttpResponse
from django.template.loader import render_to_string

from dajaxice.decorators import dajaxice_register
from app_actividad.forms import CrearActividadForm
from app_actividad.models import Actividad
from app_comentarios.models import CreadorComentario, obtener_comentarios
from app_comentarios.forms import CrearComentarioForm

@dajaxice_register
def crearActividadForm(request,data):
    form = CrearActividadForm()
    vista = render_to_string('app_actividad/crear_actividad.html',{'form':form, 'idpiz': data})
    return simplejson.dumps({'vista': vista})

@dajaxice_register
def crearSubactividadAjax(request,idact, idpiz):
    vista = render_to_string('app_actividad/crear_subactividad.html',{'idact':idact, 'idpiz': idpiz})
    return simplejson.dumps({'vista': vista})

@dajaxice_register
def mostrarActividad(request,data):
    act = Actividad.objects.get(idact = data)
    vista = render_to_string('app_actividad/vistaActividad.html', {'actividad': act})
    return simplejson.dumps({'vista': vista})

@csrf_exempt
@dajaxice_register
def crearComentario(request,form,data):
    f= CrearComentarioForm(form)
    if f.is_valid():
        datos = f.cleaned_data
        contenido = datos['contenido']
        act = Actividad.objects.get(idact = data)
        hora = datetime.time(datetime.now())
        fecha = date.today()
        usuario = request.user
        CreadorComentario(hora, fecha, contenido, act, usuario)
        act = Actividad.objects.get(idact = data)
        lista = obtener_comentarios(data)
        vista = render_to_string('app_actividad/vistaActividad.html', {'lista': lista, 'actividad': act, })
        return simplejson.dumps({'vista':vista})

    act = Actividad.objects.get(idact = data)
    lista = obtener_comentarios(data)
    vista = render_to_string('app_actividad/vistaActividad.html', {'lista': lista, 'actividad': act, })
    return simplejson.dumps({'vista':vista})

@dajaxice_register
def asignarActividadAjax(request, id_actividad, idpiz):
    vista = render_to_string('app_actividad/asignar_actividad.html', {'id_actividad': id_actividad, 'idpiz': idpiz})
    return simplejson.dumps({'vista': vista})

@dajaxice_register
def modificarActividadAjax(request, idact):
    act = Actividad.objects.get(idact=idact)
    lista = []
    lista.append(act.nombreact)
    lista.append(act.descripcionact)
    lista.append(act.fechainicial)
    lista.append(act.fechaentrega)

    vista = render_to_string('app_actividad/modificar_actividad.html', {'idact': idact, 'lista': lista})
    return simplejson.dumps({'vista': vista})
