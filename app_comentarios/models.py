import datetime
from django.db import models
from django.db.models import Max
from app_actividad.models import Actividad
from django.contrib.auth.models import User
from app_log.models import ManejadorAccion, Accion

# Create your models here.

class Comentario(models.Model):
  idcomentario = models.AutoField(primary_key=True)
  horacomentario = models.TimeField(auto_now=False,auto_now_add=False)
  fechacomentario = models.DateField(auto_now=False,auto_now_add=False)
  contenido = models.CharField(max_length=200)
  idactcomentario = models.ForeignKey(Actividad, related_name = 'comentario_idActComentario', to_field = 'idact')
  loginusuario = models.ForeignKey(User, related_name = "comentario_loginusuario")

def CreadorComentario(hora, fecha, contenido, act, usuario):
  #Obtengo el ultimo id creado y sumo 1 a su valor para el id de la nuevo comentario
#  ultimo = Comentario.objects.all().aggregate(Max('idcomentario'))
  #if ultimo['idcomentario__max'] == None:
      #idcomentario=0
  #else:
      #idcomentario= ultimo['idcomentario__max']+1

  #instancio el comentario a guardar   
  nuevoComentario = Comentario(horacomentario=hora, 
    fechacomentario=fecha, 
    contenido=contenido, 
    idactcomentario=act,
    loginusuario=usuario)
  nuevoComentario.save()

  fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
  # act = Actividad.objects.get(idact = act.idact)
  Accion.objects.crearAccion(
    usuario,
    "El usuario %s hizo un comentario en la actividad %s" % (usuario.username, act.nombreact),
    fechaYHora,
    'i')

def eliminar(idComentario, usuario, actividad):
    """
    Elimina un comentario de la tabla de comentarios
    """
    comentario = Comentario.objects.filter(idcomentario = idComentario)
    comentario.delete()

    fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # actividad = Actividad.objects.get(idact=comentario.idactcomentario)
    Accion.objects.crearAccion(
      usuario,
      "El usuario %s elimino un comentario en la actividad %s" % (usuario.username, actividad.nombreact),
      fechaYHora,
      'i')

def obtener_comentarios(idActividad):
  """
  Metodo que obtiene los comentarios de la actividad seleccionada
  """
  comentarios = Comentario.objects.filter(idactcomentario=idActividad)
  lista = []
  for elem in comentarios:
    lista.append(elem)
  return lista
