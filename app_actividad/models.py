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

def crearActividad(nombre,descript,fechaini,fechaent,piz,creador, padre):

	a=Actividad(nombreact = nombre,
       descripcionact = descript,
       fechainicial = fechaini,
       fechaentrega = fechaent,
       avanceact = 0.00,
       estadoact = 's',
       idpizactividad = piz,
       logincreador = creador,
       loginjefe = creador,
       loginasignado = creador,
       actividad_padre = padre)
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
	act = Actividad.objects.get(idact = idactividad)
	if newEstado == "c" and act.estadoact != "c":
		act.estadoact = "c"
		act.avanceact = 100
		act.save()
		calcularAvance(act.actividad_padre.idact)
		print "modifique avance"
	else:
		act.estadoact = newEstado
		act.save()

def esHoja(idact):
	act = Actividad.objects.filter(actividad_padre = idact)
	print "es hoja"
	return act.count() == 0

def cantidadHijos(idact):
	act = Actividad.objects.filter(actividad_padre = idact)
	return act.count()
	
def calcularAvance(idact):
	"""
	Actua sobre el padre, calcula el avance
	"""
	act = Actividad.objects.get(idact = idact)
	hijos = Actividad.objects.filter(actividad_padre = idact, is_active = True)
	completadas = 0
	total = 0
	for elem in hijos:
		total+= 1
		if elem.estadoact == "c":
			completadas+=1
	print completadas
	if total==1:
		for elem in hijos:
			nuevoAvance = elem.avanceact
	else:
		nuevoAvance =  ((completadas+0.00) / (total+0.00)) * 100.00
	if nuevoAvance == 100.00:
		act.estadoact = "c"
	act.avanceact = nuevoAvance
	act.save()
	if act.actividad_padre != None:
		calcularAvance(act.actividad_padre.idact)
	print "calcular avanceeeee"
	
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
	"""
	Metodo que obtiene todas las actividades de una pizarra
	"""
	act = Actividad.objects.filter(idpizactividad = idpiz, is_active = True)
	lista = []
	for elem in act:
		lista.append(elem)
	return lista
    
def obtener_subactividades(idact):
    """
    Metodo que obtiene las subactividades de una actividad
    """
    act = Actividad.objects.filter(actividad_padre=idact, is_active = True)
    lista = []
    for elem in act:
        lista.append(elem)
    return lista    

def obtener_misActividades(idpiz, usuario):
    """
    Metodo que obtiene las actividades de un usuario
    """
    act = Actividad.objects.filter(idpizactividad = idpiz, loginjefe = usuario, is_active = True)
    #lista que se retorna
    lista = []
    for elem in act:
        lista.append(elem)

    #reviso la lista para ver la contencion entre actividades, si alguna pertenece a la rama de otra, se agrega a la lista de eliminados
    eliminados = []
    for elem in lista:
        for obj in lista:
            if (obj != elem):
                hijo = esHijo(obj,elem)
                if (hijo != None):
                    if hijo not in eliminados:
                        eliminados.append(hijo)

    #Se eliminan los objetos en eliminados de lista
    for elem in eliminados:
        lista.remove(elem)
    return lista


def esHijo(act1,act2):
    """
    Metodo que determina si hijo es subactividad de padre
    """
    if (act1 == None) or (act2 == None):
        return None

    if (act1 == act2):
        return None

    if (act1.actividad_padre == act2):
        return act1
    elif (act2.actividad_padre == act1):
        return act2
    else:
        salida = esHijo(act1.actividad_padre, act2)
        if (salida != None):
            if (salida == act1.actividad_padre):
                return act1
            else:
                return act2

        salida = esHijo(act2.actividad_padre, act1)
        if (salida != None):
            if (salida == act2.actividad_padre):
                return act2
            else:
                return act1


def obtener_hijos(actividad):
    """
    Metodo que obtiene los hijos inmediatos de una actividad
    """
    hijos = Actividad.objects.filter(actividad_padre = actividad)
    lista = []
    for elem in hijos:
        lista.append(elem)

    return lista
def orden_cronologico(idpiz, loginasignado):
    """
    Metodo que ordena cronologicamente actividades de un usuario
    """
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
    """
    Metodo que ordena por estados las actividades de un usuario
    """
    #obtengo las actividades de un determinado usuario
    act = Actividad.objects.filter(idpizactividad=idpiz, loginasignado=loginasignado).order_by('-estadoact')
    lista = []

    for elem in act:
        lista.append(elem)  
    return lista
