from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from app_pizarras.forms import CrearPizarraForm
from app_actividad.models import Actividad
from app_pizarras.models import Pizarra

@dajaxice_register
def crearPizarraForm(request):
	"""
	Metodo que abre el dialogo con el form de crear pizarra
	In: request
	Out: archivo json
	Autor: Juan Arocha
	Fecha: 15-11-12 Version 1.0
	"""
	form = CrearPizarraForm()
	vista = render_to_string('app_pizarras/crear_pizarra.html',{'form':form})
	return simplejson.dumps({'vista': vista})

@dajaxice_register
def modificarPizarraAjax(request, id_pizarra):
    """
    Metodo para modificar los datos de una pizarra
    """
    pizarra = Pizarra.objects.get(idpiz = id_pizarra)
    lista = []
    lista.append(pizarra.nombrepiz)
    lista.append(pizarra.descripcionpiz)
    lista.append(pizarra.fechacreacion)
    lista.append(pizarra.fechafinal)

    #print "Nombre de la pizarra " + pizarra.nombrepiz
    #print "Descripcion de la pizarra " + pizarra.descripcion
    #print "Fecha de creacion "  + pizarra.fechacreacion
    #print "Fecha final " + pizarra.fechafinal

    vista = render_to_string('app_pizarras/modificar_pizarra.html',{'id_pizarra':id_pizarra, 'lista': lista })
    return simplejson.dumps({'vista': vista,})

