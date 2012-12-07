from django.shortcuts import render
from app_usuarios.models import UserProfile
from app_pizarras.forms import CrearPizarraForm
from app_pizarras.models import *
from app_actividad.forms import *
from app_actividad.models import *
from app_comentarios.models import *
from app_log.models import ManejadorAccion, Accion
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from app_log.models import ManejadorAccion, Accion

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
      act = Actividad.objects.get(idpizactividad = piz, actividad_padre = None)
      
      crearActividad(nombreact,descripcionact,fechainicial,fechaentrega,piz,user,act)
      calcularAvance(act.idact)

      lista = obtener_actividades(request.POST['idpiz'])
      lista = obtener_misActividades(request.POST['idpiz'], user)
      #Lista de arboles de mis actividades   
      root = []
      for elem in lista:
        root.append(Node(elem))

      for i in range(0,len(root)):
        root[i].generate_tree()
        string = '{'
        string += root[i].generate_json()
        string += '}'
        print string

      colab = colaboradores(request.POST['idpiz'])
      usuario = request.user
      orden = orden_cronologico(piz.idpiz, usuario)
      ordenE = orden_por_estados(piz.idpiz, usuario)
      return render(request,'app_pizarras/vistaPizarra.html',{ 'pizarra' : piz, 'colaboradores': colab, 'lista': lista, 'orden': orden, 'ordenE': ordenE, 'colaboradores': colab, 'arbol': string, })

    else:
      return render(request,'app_actividad/crear_actividad.html',{'form':form, 'idpiz':request.POST['idpiz']})
  
@csrf_exempt
def crear_subactividad(request):
  if request.method == 'POST':
    form = CrearActividadForm(request.POST)
    if form.is_valid():
      print "validoooooooooo "
      data = form.cleaned_data

      nombreact = data['nombre'] # NOMBRE DE LA ACTIVIDAD
      descripcionact = data['descripcion'] # DESCRIPCION DE LA ACTIVIDAD
      fechainicial = data['fecha_inicio'] # FECHA INICIAL
      fechaentrega = data['fecha_final'] # FECHA DE ENTREGA
      
      idpizactividad = request.POST['idpiz']
      pizarra = Pizarra.objects.get(idpiz=idpizactividad)
      padre = Actividad.objects.get(idact=request.POST['idact']) # IDACT.. ES OBTENER EL ID DE LA ACTIVIDAD.
      user = request.user
      
      crearActividad(nombreact,descripcionact,fechainicial,fechaentrega,pizarra,user,padre)
      calcularAvance(padre.idact)
      listasub = obtener_subactividades(request.POST['idact'])
      lista = obtener_comentarios(request.POST['idact'])
      colab = colaboradores(padre.idpizactividad.idpiz)

      usuario = request.user
      orden = orden_cronologico(idpizactividad, usuario)
      ordenE = orden_por_estados(idpizactividad, usuario)
      return render(request,'app_pizarras/vistaPizarra.html',{ 'pizarra' : pizarra, 'colaboradores': colab, 'lista': lista, 'orden': orden, 'ordenE': ordenE})
    else:
      print "invalidooooooooooooooo!"

      return render(request,'app_actividad/crear_subactividad.html',{'form': form, 'idact':request.POST['idact'],'idpiz':request.POST['idpiz']})

  
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
        act = Actividad.objects.get(idact = idact)     
        usuario = request.user
        eliminarActividad(idact, usuario)

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
        piz = act.idpizactividad
        lista = obtener_comentarios(idact)
        listasub = obtener_subactividades(idact)
        actEsHoja = esHoja(idact)
        return render(request,'app_actividad/vistaActividad.html',{ 'actividad' : act, 'lista': lista, 'listasub':listasub, 'pizarra':piz, 'actEsHoja':actEsHoja, })

    lista = obtener_actividades(request)
    return render(request, 'app_actividad/vistaActividad.html', { 'lista' : lista, })
    
    
# SUBACTIVIDADES    

def listar_subactividad(request):
    lista = obtener_subactividades(request)
    return render(request, 'app_actividad/listar.html', { 'lista' : lista, })	    
    
@csrf_exempt        
def visualizar_subactividad(request):
    if request.method== 'POST':
        idact = request.POST['idact']
        act = Actividad.objects.get(idact=idact)
        lista = obtener_subactividad(idact)
        return render(request,'app_actividad/vistaActividad.html',{ 'actividad' : act, 'lista': lista})

    lista = obtener_subactividades(request)
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
      	user = request.user
        modificarActividad(idact,nombreact,descripcionact,fechaInicial,fechaEntrega, user)
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
        if estado != "null":
            cambiarEstado(idact,estado, request.user)
        lista = obtener_comentarios(idact)
        act = Actividad.objects.get(idact = idact)
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
    
    return render(request,'app_actividad/asignar_actividad.html',{'idact':request.POST['idact'], 'idpiz':request.POST['idpiz']})

@csrf_exempt
def invitar_usuario(request):
    ##
    #Metodo que asigna una actividad a un derminado usuario
    #@author German Leon
    #@date 29-11-2012
    #@version 1.0
    #@param request
    
    if request.method == 'POST':
        id_actividad = request.POST['id_actividad']
        recipiente = request.POST['recipiente']
        id_pizarra = request.POST['idpiz']
        
        act = Actividad.objects.get(idact=id_actividad)
        piz = Pizarra.objects.get(idpiz=id_pizarra)
        nombre_pizarra = piz.nombrepiz
        print nombre_pizarra
        nombre_actividad = act.nombreact
        
        if not User.objects.filter(email=recipiente).exists():
            #   El usuario no estaba registrado se le crea un nombre de usuario y una contrasena
            
            nombre_usuario = recipiente.partition("@")[0]
            contrasena = User.objects.make_random_password()
            asunto = "Felicidades, usted ha sido invitado a participar como colaborador"
            mensaje = """
                Felicidades usted ha sido invitado a trabajar como colaborador en la actividad \"%s\" del Proyecto \"%s\"
                Su nombre de usuario es: %s
                Su contrasena es: %s

                
                Para editar su perfil visite nuestra pagina 
                
                Por su seguridad le recomendamos cambiar la clave """ % (nombre_actividad, nombre_pizarra, nombre_usuario, contrasena)
                
	    #format(unicode(usuario), unicode(contrasena))
            send_mail(asunto, mensaje, None, [recipiente],  fail_silently = False)

            #   Creamos el usuario con nombre de usuario y contrasena como unicos datos
            nuevo = User.objects.create(username=nombre_usuario, email=recipiente, first_name="", last_name="")
            print nuevo
            print "contrasena " + contrasena
            nuevo.set_password(contrasena)

            print nuevo.password
            nuevo.save()
            tel = '000'
            usuario = UserProfile.objects.create(user= nuevo, telefono=tel)

            editarAsignado(id_actividad,nuevo, request.user)
            editarJefe(id_actividad,request.user)
            
            # Acomodar el crear_colaborador con la logica del negocio 
        else:
            #   El usuario ya estaba registrado solo hace falta notificarle su asignacion por correo 
            usuario = User.objects.get(email=recipiente)
            nombre_user = usuario.first_name
            asunto = "Buen dia %s, usted ha sido seleccionado para trabajar en una actividad" % nombre_user
            mensaje = "El presente correo es para notificarle que a usted se la ha asignado la actividad \"%s\" del Proyecto \"%s\"" % (nombre_actividad, nombre_pizarra)
            send_mail(asunto, mensaje, None, [recipiente],  fail_silently = False)
            editarAsignado(id_actividad, usuario, request.user)
            editarJefe(id_actividad, usuario. request.user)
        #   Llamar a algun metodo de la app_actividad que se encargue de asignarle la actividad al usuario recien creado
        

        cambiarEstado(id_actividad, 'e', request.user)
        act = Actividad.objects.get(idact=id_actividad)

        piz = act.idpizactividad
        lista = obtener_comentarios(id_actividad)
        listasub = obtener_subactividades(id_actividad)
        return render(request,'app_actividad/vistaActividad.html',{ 'actividad' : act, 'lista': lista, 'listasub':listasub, 'pizarra':piz,})

    return render(request, 'app_actividad/asignar_actividad.html', { 'idact' : idact, }) #  Esta vista puede ser cualquier otra  

