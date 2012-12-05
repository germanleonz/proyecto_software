from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from app_pizarras.models import Pizarra

class Accion(models.Model):
    idaccionuser = models.AutoField(primary_key=True)
    tipo_errores=(('d', 'DEBUG'), ('i', 'INFO'),('w', 'WARNING'),('e', 'ERROR'),('f', 'FATAL'))
    tipo_accion = models.CharField(max_length=7, choices=tipo_errores)
    accionloginuser = models.ForeignKey(User, related_name = 'accion_user_loginuser')
    contenidoaccionuser = models.CharField(max_length=200)
    fechahoraaccionuser = models.DateTimeField(auto_now=False, auto_now_add=False)

def crearAccion(accionloginuser, contenidoaccionuser, fechahoraaccionuser, tipo_accion):
	"""
    Metodo que crea una accion referente a un usuario.
    """
	nuevo = Accion(
		accionloginuser = accionloginuser,
		contenidoaccionuser = contenidoaccionuser,
		fechahoraaccionuser = fechahoraaccionuser,
        tipo_accion = tipo_accion
		)
	nuevo.save()

def obtenerAccion(idaccionuser):
    """Metodo que retorna un diccionario con los datos de una accion asociada con el idpiz y
    el login del usuario"""
    accion = {}
    a = Accion.Objects.get(idaccionuser = idaccionuser)
    accion['accionloginuser'] = a.accionloginuser
    accion['contenidoaccionuser'] = a.contenidoaccionuser
    accion['fechahoraaccionuser'] = a.fechahoraaccionuser
    return a

def obtenerAccionesUser():
	"""
    Metodo que retorna una lista con los datos de una accion asociada al usuario
    """
	result = Accion.objects.all()
	lista = []
	for elem in result:
		lista.append(elem)
	return lista

def eliminarAccion(idaccionuser):
    """
    Metodo que elimina una accion de usuario de la base de datos
    """
    elem = Accion.objects.filter(idaccionuser = idaccionuser)
    elem.delete()

