from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from app_pizarras.forms import CrearPizarraForm
from app_actividad.models import Actividad

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
def buscarActividades(request):
    """
    Metodo que busca las subactividades de una pizarra. Guarda los nombres de las actividades
    en un arreglo de nombres de subactividades y arma un arreglo de pares (actividades,)
    In: request
    Out: archivo jsosn
    Autor: Juan Arocha
    Fecha: 10-11-12 Version 1.0
    """
    nombres = []
    for i in range (0,5):
        nombres.append(("string"+str(i),"string"+str(i+1)))
    return simplejson.dumps({'nombres': nombres, })
