from django.db import models
from django.db.models import Max
from app_pizarras.models import Pizarra
from django.contrib.auth.models import User
import re
# Create your models here.

class Actividad(models.Model):
    idact = models.IntegerField(primary_key=True)
    idpizactividad = models.ForeignKey(Pizarra,related_name='actividad_enPizarra')
    fechainicial = models.DateField(auto_now=False, auto_now_add=False)
    fechaentrega = models.DateField(auto_now=False, auto_now_add=False)
    descripcionact = models.CharField(max_length=100)
    ESTADOS=(('c', 'Completada'), ('r', 'Retrasada'),('e', 'En Ejecucion'), ('p', 'Postergada'),('s', 'Sin Asignar'))
    estadoact = models.CharField(max_length=15, choices=ESTADOS)
    avanceact = models.IntegerField()
    nombreact = models.CharField(max_length=50)
    logincreador = models.ForeignKey(User, related_name = 'actividad_loginCreador')
    loginjefe = models.ForeignKey(User, related_name = 'actividad_loginJefe')
    loginasignado = models.ForeignKey(User, related_name = 'actividad_loginAsignado')

class seDivide(models.Model):
    idactividad = models.ForeignKey(Actividad, related_name = 'seDivide_idAct')
    idsubactividad = models.ForeignKey(Actividad, related_name = 'seDivide_idSubAct')    

def crearActividad(nombre,descript,fechaini,fechaent,piz,creador):

    ult = Actividad.objects.all().aggregate(Max('idact'))
    if ult['idact__max'] == None:
        idact=0
    else:
        idact= ult['idact__max']+1

    a=Actividad(idact=idact, 
        nombreact=nombre,
        descripcionact=descript,
        fechainicial=fechaini,
        fechaentrega=fechaent,
        avanceact=0.00,estadoact='s',
        idpizactividad=piz,
        logincreador=creador,
        loginjefe=creador,
        loginasignado=creador)
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

def conseguirHijos(idpiz):
    """
    Metodo que consigue las subactividades inmediatas de una actividad padre
    """
    pass

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
        nombre = str(usuario.first_name)+" "+str(usuario.last_name)
        colaboradores.append(nombre)
        print nombre

    return colaboradores

def obtener_actividades(idpiz):
    act = Actividad.objects.filter(idpizactividad = idpiz)
    lista = []
    for elem in act:
        lista.append(elem)
    return lista

