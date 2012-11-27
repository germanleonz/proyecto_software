from django.shortcuts import render
from app_pizarras.models import *
from app_pizarras.forms import *
from app_actividad.models import colaboradores
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def crear_pizarra(request):
    """
    Metodo que crea una nueva pizarra llamando a CreadorPizarra
    """
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
            lista = obtener_pizarras(request)
            return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })
        else:
            lista = obtener_pizarras(request)
            return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })
    
    form = CrearPizarraForm()
    return render(request, 'app_pizarras/crear_pizarra.html', { 'form': form, })

@login_required
def obtener_pizarras(request):
    """
    Metodo que obtiene las pizarras del usuario logueado
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
    """
    lista = obtener_pizarras(request)
    return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })
        
@login_required
def eliminar_pizarra(request):
    """
    Metodo que elimina una pizarra de la base de datos
    """
    if request.method == 'POST':
        idpiz = request.POST['idpiz']
        eliminar(idpiz)
        lista = obtener_pizarras(request)
        return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })

    lista = obtener_pizarras(request)
    return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })

@login_required
def modificar_pizarra(request):
    """
    Metodo que sirve para modificar una pizarra de la base de datos
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
    if request.method== 'POST':
        idpiz = request.POST['idpiz']
        pi = Pizarra.objects.get(idpiz=idpiz)
        print "EPALEEEEEEEEEE"
        lista = colaboradores(idpiz)
        for elem in lista:
            print "en el views " + elem
        return render(request,'app_pizarras/vistaPizarra.html',{ 'pizarra' : pi, 'colaboradores': lista})
    
    #no se que retornar si no es post asi que retorno la vista anterior y ya
    lista = obtener_pizarras(request)
    return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })
        
