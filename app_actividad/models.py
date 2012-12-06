from django.db import models
from django.db.models import Max
from app_pizarras.models import Pizarra
from django.contrib.auth.models import User
from app_pizarras.arbol import *
from app_log.models import ManejadorAccion, Accion
import re
import datetime
# Create your models here.

class Actividad(models.Model):
    idact = models.AutoField(primary_key=True)
    idpizactividad = models.ForeignKey(Pizarra,related_name='actividad_enPizarra')
    fechainicial = models.DateField(auto_now=False, auto_now_add=False)
    fechaentrega = models.DateField(auto_now=False, auto_now_add=False)
    descripcionact = models.CharField(max_length =150)
    ESTADOS=(('c', 'Completada'), ('r', 'Retrasada'),('e', 'En Ejecucion'),('p', 'Postergada'),('s', 'Sin Asignar'))
    estadoact = models.CharField(max_length=15, choices=ESTADOS)
    avanceact = models.IntegerField()
    nombreact = models.CharField(max_length=50)
    logincreador = models.ForeignKey(User, related_name = 'actividad_loginCreador')
    loginjefe = models.ForeignKey(User, related_name = 'actividad_loginJefe')
    loginasignado = models.ForeignKey(User, related_name = 'actividad_loginAsignado')
    actividad_padre = models.ForeignKey('self', related_name='sub_actividades', null=True) # Atributo que indica el padre de la actividad, en caso de que la actividad sea la raiz entonces el padre es null
    is_active = models.BooleanField(default = True)

class seDivide(models.Model):
    idactividad = models.ForeignKey(Actividad, related_name = 'seDivide_idAct')
    idsubactividad = models.ForeignKey(Actividad, related_name = 'seDivide_idSubAct')    

def crearActividad(nombre,descript,fechaini,fechaent,piz,creador, padre):

    ult = Actividad.objects.all().aggregate(Max('idact'))
    #if ult['idact__max'] == None:
        #idact=0
    #else:
        #idact= ult['idact__max']+1
    a=Actividad(
        nombreact=nombre,
        descripcionact=descript,
        fechainicial=fechaini,
        fechaentrega=fechaent,
        avanceact=0.00,estadoact='s',
        idpizactividad=piz,
        logincreador=creador,
        loginjefe=creador,
        loginasignado=creador,
        actividad_padre= padre)
    a.save()

    #Se registra en el log la creacion de la nueva actividad
    fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")          
    Accion.objects.crearAccion(
        creador,
        "El usuario %s creo la actividad %s" % (creador.username, nombre), 
        fechaYHora, 
        'i')

def modificarActividad(idactividad, nombre, descript, fechaini, fechaent, user):
    act = Actividad.objects.filter(idact = idactividad)
    act.update(nombreact=nombre,descripcionact=descript, fechainicial=fechaini, fechaentrega=fechaent)
    fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    Accion.objects.crearAccion(
      user,
      "El usuario %s modifico la informacion de la actividad %s" % (user.username, nombre), 
      fechaYHora,
      'i')
    
def editarAsignado(idactividad, idAsignado):
    act = Actividad.objects.filter(idact = idactividad)
    act.update(loginasignado = idAsignado)
    
def editarJefe(idactividad, idJefe):
    act = Actividad.objects.filter(idact = idactividad)
    act.update(loginjefe = idJefe)

def cambiarEstado(idactividad, newEstado):
    act = Actividad.objects.filter(idact = idactividad)
    act.update(estadoact=newEstado)

def eliminarActividad(idactividad, usuario):
    act = Actividad.objects.get(idact = idactividad)
    act.is_active = False
    act.save()

    fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    Accion.objects.crearAccion(
      usuario,
      "El usuario %s elimino la actividad %s" % (usuario.username, act.nombreact), 
      fechaYHora,
      'i')

#pasar un nodo
def generar_arbol(actual): 
    """acts = Actividad.Objects.filter(actividad_padre = idact)
    for i in range (0,len(acts)):
        aux = Actividad.Objects.filter(actividad_padre = acts[i].idact)
        if len(aux)>0:
            hijo = Node(act[i].idact)
            hijo.add_child(generar_arbol(acts[i].idact,hijo))
            root.add_child(hijo)
        else:
            root.add_child(acts[i].idact)

    return root
    """
    nodo = Node(actual)
    actividades = Actividad.objects.filter(actividad_padre = actual)
    
    for i in actividades:
        nodo.add_child(generar_arbol(i.idact))

    return nodo


def colaboradores(idpiz):
    """
    Metodo que retorna los colaboradores de una pizarra
    """
    colaboradores= []
    act= Actividad.objects.filter(idpizactividad= idpiz).distinct('loginasignado')
    for elem in act:   
        persona = elem.loginasignado
        usuario = User.objects.get(username= persona)
        colaboradores.append(usuario)

    return colaboradores

def obtener_actividades(idpiz):
    act = Actividad.objects.filter(idpizactividad = idpiz)
    lista = []
    for elem in act:
        lista.append(elem)
    return lista
    
def obtener_subactividades(idact):
    act = Actividad.objects.filter(actividad_padre=idact)
    lista = []
    for elem in act:
        lista.append(elem)
    return lista    


def orden_cronologico(idpiz, loginasignado):
    #obtengo las actividades de un determinado usuario
    act = Actividad.objects.filter(idpizactividad=idpiz, loginasignado=loginasignado).order_by('-fechaentrega')
    lista = []
    aux = []

    for elem in act:
        lista.append(elem)  

    while (len(lista) >0):
        aux.append(lista.pop())

    return aux


def orden_por_estados(idpiz, loginasignado):
    #obtengo las actividades de un determinado usuario
    act = Actividad.objects.filter(idpizactividad=idpiz, loginasignado=loginasignado).order_by('-estadoact')
    lista = []

    for elem in act:
        lista.append(elem)  
    return lista

