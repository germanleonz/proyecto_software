import datetime
from datetime import date
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from app_actividad.models import Actividad
from app_comentarios.models import Comentario, CreadorComentario, eliminar, obtener_comentarios
from app_comentarios.forms import CrearComentarioForm
from app_log.models import ManejadorAccion, Accion
from app_actividad.views import visualizar_actividad

# Create your views here.

@login_required
def crear_comentario(request):
  """
  Metodo que crea un nuevo comentario llamando a CreadorComentario
  in: request
  out: salida a la vista adecuada
  """
  if request.method =='POST':
    form = CrearComentarioForm(request.POST)
    idact = request.POST['idact']
    act = Actividad.objects.get(idact = idact)
    if form.is_valid():
      data = form.cleaned_data
      
      contenido = data['contenido']
      hora = datetime.datetime.time(datetime.datetime.now())
      fecha = date.today()
      usuario = request.user
      
      CreadorComentario(hora, fecha, contenido, act, usuario)

      print idact
      lista = obtener_comentarios(idact)
      return visualizar_actividad(request)
    else:
      return visualizar_actividad(request)
  form = CrearComentarioForm()
  return visualizar_actividad(request)


@login_required
def eliminar_comentario(request):
  """
  Metodo que llama al manejador para eliminar comentario
  in request
  out salida a la vista adevuada
  """
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
