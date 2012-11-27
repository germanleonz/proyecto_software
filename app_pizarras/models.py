from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError


class Pizarra(models.Model):
    idpiz = models.IntegerField(primary_key = True)
    nombrepiz = models.CharField(max_length=50)
    descripcionpiz = models.CharField(max_length=150) 
    fechacreacion = models.DateField(auto_now=False, auto_now_add=False)
    fechafinal = models.DateField(auto_now=False, auto_now_add=False)
    avancepiz = models.IntegerField()
    logindueno = models.ForeignKey(User, related_name='pizarra_dueno')


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
    login = models.ForeignKey(User, related_name='dueno_personalizar_pizarra')
    pizarra = models.ForeignKey(Pizarra, related_name='pizarra_personalizar_pizarra')
    posicion = models.IntegerField()

"""
Metodo que guarda una pizarra en la base de datos generando la id como el siguiente al mas alto
"""

def CreadorPizarra(nombrepiz, descripcionpiz, fechacreacion, fechafinal, usuario):
    """
    Metodo que guarda una pizarra en la base de datos generando la id como el siguiente al mas alto
    """
    #Obtengo el ultimo id creado y sumo 1 a su valor para el id de la nueva pizarra
    ultima = Pizarra.objects.all().aggregate(Max('idpiz'))
    if ultima['idpiz__max'] == None:
        idpiz=0
    else:
        idpiz= ultima['idpiz__max']+1

    #instancio la pizarra a guardar   

    nuevo = Pizarra(idpiz=idpiz, nombrepiz=nombrepiz, descripcionpiz=descripcionpiz, fechacreacion=fechacreacion, fechafinal=fechafinal, avancepiz=0, logindueno =  usuario)

    nuevo.save()

def modificar(idpiz, nombrepiz, descripcionpiz, fechafinal):
    """
    Metodo que modifica una pizarra de la base de datos
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


def eliminar(idpiz):
    """
    Metodo que elimina una pizarra de la base de datos
    """
    elem = Pizarra.objects.filter(idpiz = idpiz)

    elem.delete()

def obtenerPizarra(idpiz):
    """
    Metodo que retorna un diccionario con los datos de una pizarra asociada con el idpiz
    """
    pizarra = {}
    elem = Pizarra.objects.get(idpiz = idpiz)
    pizarra['nombre'] = elem.nombrepiz
    pizarra['descripcion'] = elem.descripcionpiz
    pizarra['fechacreacion'] = elem.fechacreacion
    pizarra['fechafinal'] = elem.fechafinal
    
    return pizarra
