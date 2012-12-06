from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
#from app_actividad.models import crearActividad
from app_log.models import ManejadorAccion, Accion
import datetime
from datetime import date
from django.core.exceptions import ValidationError

class Pizarra(models.Model):
    """
    Clase pizarra, representa a la tabla de pizarra en la base de datos
    In: models.Model
    Out: --
    Autor: Oriana Gomez y Carla Urrea
    Fecha: 27-10-12 Version 1.0
    """
    idpiz = models.AutoField(primary_key = True)
    nombrepiz = models.CharField(max_length=50)
    descripcionpiz = models.CharField(max_length=150) 
    fechacreacion = models.DateField(auto_now=False, auto_now_add=False)
    fechafinal = models.DateField(auto_now=False, auto_now_add=False)
    avancepiz = models.IntegerField()
    logindueno = models.ForeignKey(User, related_name='pizarra_dueno')
    is_active = models.BooleanField(default = True)

    def save(self, *args, **kwargs):
        if self.fechacreacion < date.today():
            raise ValidationError(u'\"%s\" Error. La fecha de creacion debe ser mayor o igual a la fecha de hoy' % self.fechacreacion)
        elif self.fechafinal < self.fechacreacion:
            raise ValidationError(u'\"%s\", \"%s\" Error. La fecha final debe ser mayor o igual a la fecha de creacion' % (self.fechacreacion, self.fechafinal))
        elif self.fechafinal < date.today():
            raise ValidationError(u'\"%s\", \"%s\" Error. La fecha final debe ser mayor o igual a la fecha de hoy' % (self.fechafinal))    
        else:    
            super(Pizarra,self).save(*args,**kwargs)

class PersonalizarPizarra(models.Model):
    """
    Metodo que permite guardar las posiciones de las pizarras dentro de la pared de un usuario
    In: models.Model
    Out: --
    Autor: Oriana Gomez y Carla Urrea
    Fecha: 27-10-12 Version 1.0
    """
    login = models.ForeignKey(User, related_name='dueno_personalizar_pizarra')
    pizarra = models.ForeignKey(Pizarra, related_name='pizarra_personalizar_pizarra')
    posicion = models.IntegerField()

def CreadorPizarra(nombrepiz, descripcionpiz, fechacreacion, fechafinal, usuario):
    """
    Metodo que guarda una pizarra en la base de datos generando la id como el siguiente al mas alto
    In: nombrepiz, descripcionpiz, fechacreacion, fechafinal, usuario
    Out: --
    Autor: Juan Arocha
    Fecha: 27-10-12 Version 1.0
    """
    from app_actividad.models import crearActividad
     #instancio la pizarra a guardar   

    nuevo = Pizarra(
        nombrepiz=nombrepiz, 
        descripcionpiz=descripcionpiz,
        fechacreacion=fechacreacion,
        fechafinal=fechafinal,
        avancepiz=0,
        logindueno =  usuario)
    nuevo.save()

    #Se registra en el log la creacion de la nueva pizarra
    fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    nombre_usuario = usuario.username            
    Accion.objects.crearAccion(
        usuario,
        "El usuario %s creo la pizarra %s" % (nombre_usuario, str(nombrepiz)),
        fechaYHora,
        'i')

    #   Creamos la actividad que representa a la pizarra dentro de la pizarra   
    crearActividad(nombrepiz,descripcionpiz,fechacreacion, fechafinal, nuevo, usuario, None)

def modificar(idpiz, nombrepiz, descripcionpiz, fechafinal, usuario):
    """
    Metodo que modifica una pizarra de la base de datos
    In: idpiz, nombrepiz, descripcionpiz, fechafinal
    Out: --
    Autor: Juan Arocha
    Fecha: 27-10-12 Version 1.0
    """
    nueva = Pizarra.objects.filter(idpiz = idpiz)
    nombreB = False
    descripcionB = False
    fechafinalB = False
    if nombrepiz == "":
        nombreB = True
    if descripcionpiz == "":
        descripcionB = True
    if fechafinal == "":
        fechafinalB = True
    
    if not nombreB and not descripcionB and not fechafinalB:
        nuevapiz = nueva.get()
        nuevapiz.nombrepiz = nombrepiz
        nuevapiz.descripcionpiz = descripcionpiz
        nuevapiz.fechafinal = fechafinal
        nuevapiz.save()

        fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        nombre_usuario = usuario.username

        #Se registra en el log la creacion de la nueva pizarra
        Accion.objects.crearAccion(
            usuario,
            "El usuario %s modifico la informacion de la pizarra %s" % (nombre_usuario, str(nombrepiz)), 
            fechaYHora,
            'i')   



def eliminar(idpiz):
    """
    Metodo que elimina una pizarra de la base de datos
    In: idpiz
    Out: --
    Autor: Juan Arocha
    Fecha: 27-10-12 Version 1.0
    """
    from app_actividad.models import Actividad
    
    elem = Pizarra.objects.get(idpiz = idpiz)
    elem.is_active = False
    elem.save()
    usuario = User.objects.get(username=elem.logindueno)
    
    act = Actividad.objects.filter(idpizactividad = idpiz, is_active = True)
    lista = []
    for elem in act:
    	elem.is_active = False
	elem.save()

    #Se registra en el log la creacion de la nueva pizarra
    fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    Accion.objects.crearAccion(
        usuario,
        "El usuario %s elimino la pizarra %s" % (usuario.username, str(elem.nombrepiz)), 
        fechaYHora,
        'w')       
    

def obtenerPizarra(idpiz):
    """
    Metodo que retorna un diccionario con los datos de una pizarra asociada con el idpiz
    In: idpiz
    Out: pizarra
    Autor: Juan Arocha
    Fecha: 27-10-12 Version 1.0
    """
    pizarra = {}
    elem = Pizarra.objects.get(idpiz = idpiz)
    pizarra['nombre'] = elem.nombrepiz
    pizarra['descripcion'] = elem.descripcionpiz
    pizarra['fechacreacion'] = elem.fechacreacion
    pizarra['fechafinal'] = elem.fechafinal
    
    return pizarra

def obtener_pizarras(usuario):
    """
    Metodo que obtiene las pizarras del usuario logueado
    In: usuario
    Out: lista
    Autor: Juan Arocha
    Fecha: 4-11-12 Version 1.0
    """
    pi = Pizarra.objects.filter(logindueno=usuario, is_active=True)
    lista = []
    for elem in pi:
        lista.append(elem)
    return lista


