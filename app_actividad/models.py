from django.db import models
from django.db.models import Max
from app_pizarras.models import Pizarra
from django.contrib.auth.models import User
from app_pizarras.arbol import *
import re
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

def modificarActividad(idactividad, nombre, descript, fechaini, fechaent):
    act = Actividad.objects.filter(idact = idactividad)
    act.update(nombreact=nombre,descripcionact=descript, fechainicial=fechaini, fechaentrega=fechaent)

def cambiarEstado(idactividad, newEstado):
    act = Actividad.objects.filter(idact = idactividad)
    act.update(estadoact=newEstado)

def eliminarActividad(idactividad):
    act = Actividad.objects.filter(idact = idactividad)
    act.delete()

def obtenerActividad(idpiz):
    actividad = {}
    act = Actividad.Objects.get(idpizactividad = idpiz)
    actividad['nombre'] = act.nombreact
    actividad['descripcion'] = act.descripcionact
    actividad['fechainicial'] = act.fechainicial
    actividad['fechaentrega'] = act.fechaentrega
    return actividad

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


def obtenerSubactividad(idact,idpiz):
    actividad = {}
    act = Actividad.Objects.get(idpizactividad = idpiz, actividad_padre=idact)
    actividad['nombre'] = act.nombreact
    actividad['descripcion'] = act.descripcionact
    actividad['fechainicial'] = act.fechainicial
    actividad['fechaentrega'] = act.fechaentrega
    return actividad
 
def conseguirHijos(idpiz):
    """
    Metodo que consigue las subactividades inmediatas de una actividad padre
    """
    hijos = list(SeDivide.objects.filter(idactividad= idpiz))
    return hijos

def conseguirSubactividades(idpiz):
    """
    Metodo que consigue todas las subactividades de una actividad principal(pizarra) y que consigue todos 
    los arcos entre dos de esas actividades que esten relacionadas
    """
    subactividades = conseguirHijos(idpiz)
    nodos_pendientes = subactividades
    prox = nodos.pendientes.pop()
    while (prox is not None):
        subs += conseguirHijos
        nodosPendientes += conseguirHijos
        #prox = 
        
    return subactividades, pares

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

