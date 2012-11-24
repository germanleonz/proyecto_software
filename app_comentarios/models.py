from django.db import models
from django.db.models import Max
from app_actividad.models import Actividad
from django.contrib.auth.models import User

# Create your models here.

class Comentario(models.Model):
  idcomentario = models.IntegerField(primary_key=True)
  horacomentario = models.TimeField(auto_now=False,auto_now_add=False)
  fechacomentario = models.DateField(auto_now=False,auto_now_add=False)
  contenido = models.CharField(max_length=200)
  idactcomentario = models.ForeignKey(Actividad, related_name = 'comentario_idActComentario', to_field = 'idact')
  loginusuario = models.ForeignKey(User, related_name = "comentario_loginusuario")

def CreadorComentario(hora, fecha, contenido, idact,usuario):
  #Obtengo el ultimo id creado y sumo 1 a su valor para el id de la nuevo comentario
  ultimo = Comentario.objects.all().aggregate(Max('idcomentario'))
  if ultimo['idcomentario__max'] == None:
      idcomentario=0
  else:
      idcomentario= ultimo['idcomentario__max']+1

  #instancio el comentario a guardar   
  nuevoComentario = Comentario(idcomentario=idcomentario, horacomentario=hora, fechacomentario=fecha, contenido=contenido, idactcomentario=idact,loginusuario=usuario)
  nuevoComentario.save()

def eliminar(idComentario):
  comentario = Comentario.objects.filter(idcomentario = idComentario)
  comentario.delete()


def obtener_comentarios(idActividad):
  """
  Metodo que obtiene los comentarios de la actividad seleccionada
  """
  comentarios = Comentario.objects.filter(idactcomentario=idActividad)
  lista = []
  for elem in comentarios:
    lista.append(elem)
  return lista