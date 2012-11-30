import datetime
from django.shortcuts import render
from app_pizarras.models import *
from app_pizarras.forms import *
from app_actividad.models import colaboradores, obtener_actividades, orden_cronologico, orden_por_estados
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from app_log.models import crearAccionUser
from app_pizarras.arbol import *
from app_actividad.models import generar_arbol

@csrf_exempt
@login_required
def crear_pizarra(request):

    if request.method == 'POST':
        #solucion temporal al problema del formato de fecha
        form = CrearPizarraForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #Variables que se pasaran al metodo CreadorPizarra
            nombrepiz = data['nombre']
            descripcionpiz = data['descripcion']
            fechaCreacion = data['fecha_inicio']
            fechaFinal = data['fecha_final']
            #Se obtiene el usuario actual para ponerlo de creador (verificar)
            usuario = request.user
            #Metodo que guarda la pizarra en la base de datos.
            CreadorPizarra(nombrepiz,descripcionpiz,fechaCreacion,fechaFinal,usuario)

            #Se registra en el log la creacion de la nueva pizarra
            fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            nombre_usuario = usuario.username            
            crearAccionUser(usuario,"El usuario %s creo la pizarra %s en la fecha %s" % (nombre_usuario, str(nombrepiz), str(fechaYHora)), fechaYHora)

            lista = obtener_pizarras(request)
            return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })
        else:
            print "NOO"
            return listar_pizarra(request)
    
    print "YAA"
    form = CrearPizarraForm()
    return render(request, 'app_pizarras/crear_pizarra.html', { 'form': form, })

@login_required
def obtener_pizarras(request):
    """
    Metodo que obtiene las pizarras del usuario logueado
    In: request
    Out: --
    Autor: Juan Arocha
    Fecha: 4-11-12 Version 1.0
    """
    usuario = request.user
    pi = Pizarra.objects.filter(logindueno=usuario)
    lista = []
    for elem in pi:
        lista.append(elem)
    return lista

@login_required
def listar_pizarra(request):
    """
    Metodo que lista las pizarras en la pared 
    In: request
    Out: --
    Autor: Juan Arocha
    Fecha: 4-11-12 Version 1.0
    """
    lista = obtener_pizarras(request)
    return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })
        
@login_required
def eliminar_pizarra(request):
    """
    Metodo que elimina una pizarra de la base de datos
    In: request
    Out: vista de listar pizarras
    Autor: Juan Arocha
    Fecha: 4-11-12 Version 1.0
    """
    if request.method == 'POST':
        idpiz = request.POST['idpiz']
        pizarra = Pizarra.objects.get(idpiz=idpiz)
        fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        usuario = request.user
        nombre_usuario = usuario.username
        nombrepiz = pizarra.nombrepiz

        #Se registra en el log la creacion de la nueva pizarra
        crearAccionUser(usuario,"El usuario %s elimino la pizarra %s en la fecha %s" % (nombre_usuario, str(nombrepiz), str(fechaYHora)), fechaYHora)        
        eliminar(idpiz)
        lista = obtener_pizarras(request)
        return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })

    
    
    lista = obtener_pizarras(request)
    return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })

@login_required
def modificar_pizarra(request):
    """
    Metodo que sirve para modificar una pizarra de la base de datos
    In: request
    Out: vista listar pizarras o vista modificar perfil
    Autor: Juan Arocha
    Fecha: 4-11-12 Version 1.0
    """
    if request.method == 'POST':
        if request.POST.__contains__('nombre'):
            form = ModificarPizarraForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                #Variables que se pasaran al metodo CreadorPizarra
                for elem in data:
                    print elem
                idpiz = request.POST['idpiz']
                nombrepiz = data['nombre']
                descripcionpiz = data['descripcion']
                fechaFinal = data['fecha_final']
                #Metodo que guarda la pizarra en la base de datos.
                modificar(idpiz,nombrepiz,descripcionpiz,fechaFinal)

                fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                usuario = request.user
                nombre_usuario = usuario.username

                #Se registra en el log la creacion de la nueva pizarra
                crearAccionUser(usuario,"El usuario %s modifico la informacion de la pizarra %s en la fecha %s" % (nombre_usuario, str(nombrepiz), str(fechaYHora)), fechaYHora)        


                lista = obtener_pizarras(request)
                return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })
            else:
                print "form no valido"
                idpiz = request.POST['idpiz']
                lista = []
                lista.append(request.POST['nombre'])
                lista.append(request.POST['descripcion'])
                lista.append(request.POST['fechafinal'])
                return render(request, 'app_pizarras/modificar_pizarra.html', { 'form': form, 'idpiz' : idpiz, 'lista' : lista })

    
@login_required
def generar_form_modificar(request):
    """
    Metodo que genera el form de modificar
    In: request
    Out: vista modificar pizarras o visa de listar pizarras
    Autor: Juan Arocha
    Fecha: 4-11-12 Version 1.0
    """
    if request.method == 'POST':
        idpiz = request.POST['idpiz']
        lista = []
        lista.append(request.POST['nombrepiz'])
        lista.append(request.POST['descripcionpiz'])
        lista.append(request.POST['fechafinal'])
        return render(request, 'app_pizarras/modificar_pizarra.html', { 'idpiz' : idpiz, 'lista' : lista })

    lista = obtener_pizarras(request)
    return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })

@login_required
def visualizar_pizarra(request):
    """
    Metodo que permite consultar la pizarra y ver sus atributos
    In: request
    Out: vista pizarra o visra listar usuarios
    Autor: Juan Arocha
    Fecha: 4-11-12 Version 1.0
    """
    
    if request.method== 'POST':
        idpiz = request.POST['idpiz']
        pi = Pizarra.objects.get(idpiz=idpiz)
        colab = colaboradores(idpiz)
        lista = obtener_actividades(request.POST['idpiz'])
        #probando con ordenar cronologicamente
        usuario = request.user
        orden = orden_cronologico(idpiz, usuario)
        ordenE = orden_por_estados(idpiz, usuario)
        return render(request,'app_pizarras/vistaPizarra.html',{ 'pizarra' : pi, 'colaboradores': colab, 'lista': lista, 'orden': orden, 'ordenE': ordenE})
    

    #no se que retornar si no es post asi que retorno la vista anterior y ya
    return listar_pizarra(request)
        
