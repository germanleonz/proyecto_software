from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from app_pizarras.models import Pizarra


class AccionUser(models.Model):
    idaccionuser = models.AutoField(primary_key=True)
    accionloginuser = models.ForeignKey(User, related_name = 'accion_user_loginuser')
    contenidoaccionuser = models.CharField(max_length=200)
    fechahoraaccionuser = models.DateTimeField(auto_now=False, auto_now_add=False)


def crearAccionUser(accionloginuser, contenidoaccionuser, fechahoraaccionuser):
	
	"""Metodo que crea una accion referente a un usuario."""

	nuevo = AccionUser(
		accionloginuser = accionloginuser,
		contenidoaccionuser = contenidoaccionuser,
		fechahoraaccionuser = fechahoraaccionuser
		)
	nuevo.save()

def obtenerAccionUser(idaccionuser):
    """Metodo que retorna un diccionario con los datos de una accion asociada con el idpiz y
    el login del usuario"""

    accion = {}
    a = AccionUser.Objects.get(idaccionuser = idaccionuser)
    accion['accionloginuser'] = a.accionloginuser
    actividad['contenidoaccionuser'] = a.contenidoaccionuser
    actividad['fechahoraaccionuser'] = a.fechahoraaccionuser

    return a

def obtenerAccionesUser():
	"""Metodo que retorna una lista con los datos de una accion asociada al usuario"""
	result = AccionUser.objects.all()
	lista = []
	for elem in result:
		lista.append(elem)

	return lista


def eliminarAccionUser(idaccionuser):
    """
    Metodo que elimina una accion de usuario de la base de datos
    """
    elem = AccionUser.objects.filter(idaccionuser = idaccionuser)

    elem.delete()

########################## Acciones sobre Pizarras ####################

# def crearAccionPizarra(loginuserpiz, contenidoaccionpiz, fechahoraaccionpiz):
	
# 	"""Metodo que crea una accion referente a una pizarra."""

# 	nuevo = AccionPizarra(
# 		loginuserpiz = loginuserpiz,
# 		contenidoaccionpiz = contenidoaccionpiz,
# 		fechahoraaccionpiz = fechahoraaccionpiz
# 		)

# 	nuevo.save()

# def obtenerAccionPizarra(idaccionpiz):
#     """Metodo que retorna un diccionario con los datos de una accion asociada con el idpiz y
#     el login del usuario"""

#     accion = {}
#     a = AccionPizarra.Objects.get(idaccionpiz = idaccionpiz)
#     accion['loginuserpiz'] = a.loginuserpiz
#     actividad['contenidoaccionpiz'] = a.contenidoaccionpiz
#     actividad['fechahoraaccionpiz'] = a.fechahoraaccionpiz

#     return a

# def obtenerAccionesPiz(idaccionpiz):
# 	"""Metodo que retorna una lista con los datos de una accion asociada a una pizarra"""
# 	accion = []
# 	acciones = AccionPizarra.objects.get(idaccionpiz = idaccionpiz)
# 	for a in acciones:
# 		lista.append(a)

# 	return lista


# def eliminarAccionPiz(idaccionuser):
#     """
#     Metodo que elimina una accion de una pizarra de la base de datos
#     """
#     elem = AccionPizarra.objects.filter(idaccionpiz = idaccionpiz)

#     elem.delete()