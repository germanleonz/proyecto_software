import datetime
from django.db import models
from django.db.models import Max
from app_actividad.models import Actividad
from django.contrib.auth.models import User
from app_log.models import ManejadorAccion, Accion

# Create your models here.

"""
Clase para la tabla de los comentarios
atributo idcomentario: id del comentario
atributo horacomentario: hora del comentario
atributo fechacomentario: fecha del comentario
atributo contenido: contenido del comentario
atributo idactcomentario: id de la actividad a la que pertenece el comentario
atributo loginusuario: usuario creador del comentario
"""
class Comentario(models.Model):
  idcomentario = models.AutoField(primary_key=True)
  horacomentario = models.TimeField(auto_now=False,auto_now_add=False)
  fechacomentario = models.DateField(auto_now=False,auto_now_add=False)
  contenido = models.CharField(max_length=200)
  idactcomentario = models.ForeignKey(Actividad, related_name = 'comentario_idActComentario', to_field = 'idact')
  loginusuario = models.ForeignKey(User, related_name = "comentario_loginusuario")


def CreadorComentario(hora, fecha, contenido, act, usuario):
  """
  Metodo que guarda en BD un nuevo comentario
  param hora: hora del comentario
  param fecha: fecha del comentario
  param contenido: contenido del comentario
  param act: actividad a la que pertenece el comentario
  param usuario: usuario que escribio el comentario
  autor: Ivan Travecedo
  fecha: 20/11/2012
  version: 1.0
  """ 
  nuevoComentario = Comentario(horacomentario=hora, fechacomentario=fecha, contenido=contenido, idactcomentario=act,loginusuario=usuario)
  nuevoComentario.save()
  fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
  Accion.objects.crearAccion(
    usuario,
    "El usuario %s hizo un comentario en la actividad %s" % (usuario.username, act.nombreact),
    fechaYHora,
    'i')

def eliminar(idComentario, usuario, actividad):
    """
    Elimina un comentario de la tabla de comentarios
    param idComentario: id del comentario a eliminar
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
  param idActividad: id de la actividad de la cual se obtendran comentarios
  out lista: Lista con los comentarios de la actividad
  """
  comentarios = Comentario.objects.filter(idactcomentario=idActividad)
  lista = []
  for elem in comentarios:
    lista.append(elem)
  return lista
