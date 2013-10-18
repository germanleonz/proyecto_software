#coding=utf-8

import datetime
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class ManejadorAccion(models.Manager):
    """
    Clase ManejadorAccion, representa el manejador de las acciones que generan logs.
    In: models.Manager
    Out: --
    Autor: Carla Urrea
    Fecha: 28-11-12 Version 1.0
    """
    def crearAccion(self,accionloginuser, contenidoaccionuser, tipo_accion):
        """
        Metodo para crear una accion de log
        In: self, accionloginuser, contenidoaccionuser, fechahoraaccionuser, tipo_accion
        Out: --
        Autor: Carla Urrea
        Fecha: 28-11-12 Version 1.0
        """
        fechahoraaccionuser = datetime.now().strftime("%Y-%m-%d %H:%M")
    	nuevo = self.model(
    		accionloginuser     = accionloginuser,
    		contenidoaccionuser = contenidoaccionuser,
    		fechahoraaccionuser = fechahoraaccionuser,
            tipo_accion         = tipo_accion
    		)
    	nuevo.save()

    def obtenerAccion(idaccionuser):
        """
        Metodo para obtener una accion de log
        In: idaccionuser
        Out: Accion a
        Autor: Carla Urrea
        Fecha: 28-11-12 Version 1.0
        """
        accion = {}
        a      = Accion.Objects.get(idaccionuser = idaccionuser)
        accion['accionloginuser']     = a.accionloginuser
        accion['contenidoaccionuser'] = a.contenidoaccionuser
        accion['fechahoraaccionuser'] = a.fechahoraaccionuser
        return a

    @classmethod
    def obtenerAcciones(cls):
        """
        Metodo para obtener acciones de log
        In: cls
        Out: lista
        Autor: Carla Urrea
        Fecha: 28-11-12 Version 1.0
        """
    	result = Accion.objects.all()
    	lista = []
    	for elem in result:
    		lista.append(elem)
    	return lista

    def eliminarAccion(idaccionuser):
        """
        Metodo para eliminar una accion de log
        In: idaccionuser
        Out: --
        Autor: Carla Urrea
        Fecha: 28-11-12 Version 1.0
        """
        elem = Accion.objects.filter(idaccionuser = idaccionuser)
        elem.delete()

class Accion(models.Model):
    """
    Clase Accion, representa a la tabla de logs en la base de datos
    In: models.Model
    Out: --
    Autor: Carla Urrea
    Fecha: 28-11-12 Version 1.0
    """
    idaccionuser        = models.AutoField(primary_key = True)
    tipo_errores        = (('d', 'DEBUG'), ('i', 'INFO'),('w', 'WARNING'),('e', 'ERROR'),('f', 'FATAL'))
    tipo_accion         = models.CharField(max_length = 7, choices = tipo_errores)
    accionloginuser     = models.ForeignKey(User, related_name = 'accion_user_loginuser')
    contenidoaccionuser = models.CharField(max_length = 200)
    fechahoraaccionuser = models.DateTimeField(auto_now = False, auto_now_add = False)

    objects = ManejadorAccion()
