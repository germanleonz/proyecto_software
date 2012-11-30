from django.shortcuts import render
from app_pizarras.forms import CrearPizarraForm
from app_pizarras.models import *
from app_actividad.forms import *
from app_actividad.models import *
from app_comentarios.models import *
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

#requiere permisos para agregar actividad
#@permission_required('app_pizarras.add_actividad')
"""
Falta arreglar este metodo para que guarde los datos de los usuraios involucrados
"""
@csrf_exempt
def crear_actividad(request):
  if request.method == 'POST':
    form = CrearActividadForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data

      nombreact = data['nombre']
      descripcionact = data['descripcion']
      fechainicial = data['fecha_inicio']
      fechaentrega = data['fecha_final']

      piz=Pizarra.objects.get(idpiz=request.POST['idpiz'])
      user = request.user

      crearActividad(nombreact,descripcionact,fechainicial,fechaentrega,piz,user)
      lista = obtener_actividades(request.POST['idpiz'])
      colab = colaboradores(request.POST['idpiz'])
      return render(request,'app_pizarras/vistaPizarra.html', {'lista' : lista, 'pizarra': piz, 'colaboradores': colab })
    else:
      return render(request,'app_actividad/crear_actividad.html',{'form':form, 'idpiz':request.POST['idpiz']})
  
def form_crear(request):
    """
    Metodo que genera el form crear
    """
    if request.method == 'POST':
        idpiz = request.POST['idpiz']
        form = CrearActividadForm()	
        return render(request, 'app_actividad/crear_actividad.html', { 'idpiz' : idpiz, 'form' : form })

    lista = obtener_actividades(request)
    return render(request, 'app_actividad/listar.html', { 'lista' : lista, })
	    
def listar_actividad(request):
    lista = obtener_actividades(request)
    return render(request, 'app_actividad/listar.html', { 'lista' : lista, })		
      
def eliminar_actividad(request):

    if request.method == 'POST':
        idact = request.POST['idact']
        idpiz = request.POST['idpiz']
        piz = Pizarra.objects.get(idpiz = idpiz)
        eliminarActividad(idact)
        colab = colaboradores(idpiz)
        lista = obtener_actividades(idpiz)
        return render(request, 'app_pizarras/vistaPizarra.html', { 'lista' : lista, 'pizarra': piz, 'colaboradores': colab})

    lista = obtener_actividades(request)
    return render(request, 'app_actividad/listar.html', { 'lista' : lista, })   
        
@csrf_exempt        
def visualizar_actividad(request):
    if request.method== 'POST':
        idact = request.POST['idact']
        act = Actividad.objects.get(idact=idact)
        return render(request,'app_actividad/vistaActividad.html',{ 'actividad' : act})

    lista = obtener_actividades(request)
    return render(request, 'app_actividad/vistaActividad.html', { 'lista' : lista, })
    

@csrf_exempt
@login_required
def modificar_actividad(request):
  """
  Metodo que sirve para modificar una pizarra de la base de datos
  """
  if request.method == 'POST':
    if request.POST.__contains__('idact'):
      form = ModificarActividadForm(request.POST)
      if form.is_valid():
	print "entre form validooooooooo"
	data = form.cleaned_data
	#Variables que se pasaran al metodo CreadorPizarra
	for elem in data:
	  print elem
	idact = request.POST['idact']
	nombreact = data['nombreact']
	descripcionact = data['descripcionact']
	fechaInicial = data['fechainicial']
	fechaEntrega = data['fechaentrega']
	act = Actividad.objects.get(idact = idact)
	#Metodo que guarda la pizarra en la base de datos.
	modificarActividad(idact,nombreact,descripcionact,fechaInicial,fechaEntrega)
	act = Actividad.objects.get(idact = idact)
	lista = obtener_comentarios(idact)
	return render(request, 'app_actividad/vistaActividad.html', { 'lista' : lista, 'actividad': act})
      else:
	print "form no valido"
	idact = request.POST['idact']
	lista = []
	lista.append(request.POST['nombreact'])
	lista.append(request.POST['descripcionact'])
	lista.append(request.POST['fechainicial'])
	lista.append(request.POST['fechaentrega'])
	return render(request, 'app_actividad/modificar_actividad.html', { 'form': form, 'idact' : idact, 'lista' : lista })
	
@csrf_exempt	
@login_required
def cambiar_estado_actividad(request):
  if request.method == 'POST':
    idact = request.POST['idact']
    estado = request.POST['estadoact']
    print "holaaaaaaaaaa soy idact",
    print idact
    act = Actividad.objects.get(idact = idact)
    if estado != "null":
      cambiarEstado(idact,estado)
    lista = obtener_comentarios(idact)
    return render(request, 'app_actividad/vistaActividad.html', { 'lista' : lista, 'actividad': act})

@csrf_exempt
@login_required
def generar_form_modificar(request):
    """
    Metodo que genera el form de modificar
    """
    if request.method == 'POST':
        idact = request.POST['idact']
        lista = []
        lista.append(request.POST['nombreact'])
        lista.append(request.POST['descripcionact'])
        lista.append(request.POST['fechainicial'])
        lista.append(request.POST['fechaentrega'])
        return render(request, 'app_actividad/modificar_actividad.html', { 'idact' : idact, 'lista' : lista })

    lista = obtener_actividades(request)
    return render(request, 'app_actividad/listar.html', { 'lista' : lista, })
    
def asignar_actividad(request):
    print 'hola'
    return render(request, 'app_actividad/asignar_actividad.html')

def invitar_usuario(request):
    """
    Metodo que invita a un colaborador a hacerse responsable de una actividad
    parametros: id_actividad a la que se le esta asignando un responsable y correo 
    de la persona a la que se le esta asignando 
    """
    if request.method == 'POST':
        id_actividad = request.post['idact']
        recipiente = request.post['recipiente']
        if User.objects.filter(email=recipiente).exists():
            #   El usuario no estaba registrado se le crea un nombre de usuario y una contrasena
            nombre_usuario = recipiente.partition("@")[0]  
            contrasena = User.object.make_random_password()
            asunto = "Felicidades, usted ha sido invitado a participar como colaborador"
            mensaje = """
                Felicidades usted ha sido invitado a trabajar como colaborador en un actividad 
                Su nombre de usuario es: {0} 
                Su contrasena es: {1}

                Por su seguridad le recomendamos cambiar la clave tan pronto como le sea posible
            """.format(unicode(usuario), unicode(contrasena))
            send_mail(asunto, mensaje, None, [recipiente],  fail_silently = False)

            #   Creamos el usuario con nombre de usuario y contrasena como unicos datos
            usuario = User.objects.create(username=nombre_usuario)
            usuario.set_password(contrasena)
            usuario.save()

            datos = {}
            datos['telefono'] = ""
            crear_colaborador(usuario, datos)
        else:
            #   El usuario ya estaba registrado solo hace falta notificarle su asignacion por correo 
            usuario = User.objects.get(email=recipiente)
            asunto = "Buen dia, usted ha sido seleccionado para trabajar en una actividad"
            mensaje = "El presente correo es para notificarle que a usted se la ha asignado una actividad de su empresa"
            send_mail(asunto, mensaje, None, [recipiente],  fail_silently = False)
        #   Llamar a algun metodo de la app_actividad que se encargue de asignarle la actividad al usuario recien creado
        lista = app_pizarras.views.obtener_pizarras(request)
        return render(request, 'app_pizarras/listar.html', { 'lista' : lista, }) #  Esta vista puede ser cualquier otra  
    return render(request, 'app_pizarras/asignar_actividad.html', { 'idact' : idact, }) #  Esta vista puede ser cualquier otra  
    
