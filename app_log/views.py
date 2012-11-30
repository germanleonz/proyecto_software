from django.shortcuts import render
from app_pizarras.models import *
from app_log.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required
def listar_accion_user(request):
	""" 
    Metodo que lista las acciones de un determinado usuario
    """

    lista = obtenerAccionesUser(request)
    return render(request, 'app_log/listarAccionUser.html', { 'lista' : lista, })

        
@login_required
def eliminar_accion_user(request):
    """
    Metodo que elimina una accion de la base de datos
    """
    if request.method == 'POST':
        idaccionuser = request.POST['idaccionuser']
        eliminarAccionUser(idaccionuser)
        lista = obtenerAccionesUser(request)
        return render(request, 'app_log/listarAccionUser.html', { 'lista' : lista, })

    lista = obtenerAccionesUser(request)
    return render(request, 'app_log/listarAccionUser.html', { 'lista' : lista, })


@login_required
def visualizar_accion_user(request):
	"""Metodo que permite la visualizacion de las acciones de usuarios"""

    if request.method== 'POST':
        idaccionuser = request.POST['idaccionuser']
        a = AccioneUser.objects.get(idaccionuser=idaccionuser)
        
        lista = obtenerAccionesUser(request)

        return render(request, 'app_log/listarAccionUser.html',{'lista': lista})


########### Acciones de Pizarras ################

@login_required
def listar_accion_piz(request):
	""" 
    Metodo que lista las acciones relacionadas a una pizarra
    """

    lista = obtenerAccionesPiz(request)
    return render(request, 'app_log/listarAccionPiz.html', { 'lista' : lista, })

        
@login_required
def eliminar_accion_piz(request):
    """
    Metodo que elimina una accion de la base de datos
    """
    if request.method == 'POST':
        idaccionpiz = request.POST['idaccionpiz']
        eliminarAccionPiz(idaccionpiz)
        lista = obtenerAccionesPiz(request)
        return render(request, 'app_log/listarAccionPiz.html', { 'lista' : lista, })

    lista = obtenerAccionesPiz(request)
    return render(request, 'app_log/listarAccionPiz.html', { 'lista' : lista, })


@login_required
def visualizar_accion_piz(request):

	"""Metodo que permite la visualizacion de las acciones de pizarras"""

    if request.method== 'POST':
        idaccionpiz = request.POST['idaccionpiz']
        a = AccionePizarra.objects.get(idaccionpiz=idaccionpiz)
        
        lista = obtenerAccionesPiz(request)

        #no se que va aqui aun
        return render(request, 'app_log/listarAccionesPiz.html',{'lista': lista})