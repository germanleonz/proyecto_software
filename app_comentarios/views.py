import datetime
from datetime import date
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from app_actividad.models import Actividad
from app_comentarios.models import Comentario, CreadorComentario, eliminar, obtener_comentarios
from app_comentarios.forms import CrearComentarioForm
from app_log.models import ManejadorAccion, Accion

# Create your views here.

@login_required
def crear_comentario(request):
  """
  Metodo que crea un nuevo comentario llamando a CreadorComentario
  """
  if request.method =='POST':
    form = CrearComentarioForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      
      contenido = data['contenido']
      idact = request.POST['idact']
      act = Actividad.objects.get(idact = idact)
      hora = datetime.datetime.time(datetime.datetime.now())
      fecha = date.today()
      usuario = request.user
      
      CreadorComentario(hora, fecha, contenido, act, usuario)

      print idact
      lista = obtener_comentarios(idact)
      return render (request,'app_actividad/vistaActividad.html',{'lista' : lista, 'actividad': act,})
    else:
      return render (request,'app_actividad/vistaActividad.html',{'form': form, 'actividad': act,})
  form = CrearComentarioForm()
  return render(request, 'app_actividad/vistaActividad.html', { 'form': form, })


@login_required
def eliminar_comentario(request):
  if request.method == 'POST':
    #   Eliminamos el comentario que se selecciono
    idComentario = request.POST['idcomentario']
    print "Eliminando comentario %s" % idComentario
    comentario = Comentario.objects.get(idcomentario=idComentario)
    print "idActComentario "+str(comentario.idactcomentario.idact)
    idActividad = comentario.idactcomentario.idact
    actividad = Actividad.objects.get(idact = idActividad)
    
    if actividad.loginjefe == request.user or actividad.loginasignado == request.user or actividad.logincreador == request.user or comentario.loginusuario == request.user:
      eliminar(idComentario, request.user, actividad)
    lista = obtener_comentarios(idActividad)
    return render(request, 'app_actividad/vistaActividad.html', { 'lista' : lista, 'actividad': actividad,})


@login_required
def listar_comentarios(request):
  """
  Metodo que lista los comentarios en la pared 
  """
  lista = obtener_comentarios(request)
  return render(request, '', { 'lista' : lista, })
