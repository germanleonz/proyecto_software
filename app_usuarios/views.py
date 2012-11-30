import re
import app_pizarras
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import views as views_admin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app_usuarios.models import UserProfile
from app_usuarios.forms import LoginForm, CrearUsuarioForm, ModificarUsuarioForm, CambiarContrasenaForm
from app_pizarras.views import listar_pizarra

def login_if(request):
    """
    Metodo que veirifica si el usuario ya esta conectado al sistema, de manera 
    que no le muestre la pagina de login, sino la de listar pizarras
    """
    if request.user.is_authenticated():
        return listar_pizarra(request)
    else:
        return login_usuario(request)

def login_usuario(request):
	"""	
	Metodo que verificar las credenciales del usuario y permite o no el acceso
	sistema
	In: request
	Out: vista login
	Autor: German Leon 
	Fecha: 5-11-12 Version 1.0
	"""
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			nombre_usuario = form.cleaned_data['nombre_usuario']
			password = form.cleaned_data['password']
			usuario = authenticate(username=nombre_usuario, password=password)
			if usuario is not None:
				#   El usuario se autentico correctamente
				if usuario.is_active:
					#   Redirigir a pagina de login correcto (ver pared)
					print "Acceso permitido para %s" % nombre_usuario
					login(request, usuario)
					lista = app_pizarras.views.obtener_pizarras(request)
					return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })
				else:
					#   Devolver un mensaje de cuenta deshabilitada
					pass
			else:
				#   Devolver un mensaje de usuario o contrasena incorrectas
				print "Acceso denegado para %s" % nombre_usuario
				print "-----" + str(User.objects.filter(username = nombre_usuario))
				#   Aqui se deben levantar los errores
				return render(request, 'app_usuarios/login.html', { 'form': form, })
	else:
		# An Unbound Form (formulario sin datos)
		form = LoginForm()  
	return render(request, 'app_usuarios/login.html', { 'form': form, })

def perfil_usuario(request):
    if request.method == 'POST':
        id = request.POST['usuario']
        usuario = User.objects.get(username=id)
        user = UserProfile.objects.get(user=usuario)
        print user.user
        return render(request, 'app_usuarios/perfil.html', { 'usuario': usuario, 'userprofile':user })


@csrf_exempt
@login_required
@permission_required('auth.create_user')
def crear_usuario(request):
    """
    Metodo para crear un usuario con los datos debidamente validados 
    proporcionados por el usuario
    In: request
    Out: vista crear usuario
    Autor: German Leon
    Fecha: 5-11-12 Version 1.0
    """
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            nombre_usuario = data['nuevo_nombre_usuario']
   
            if not User.objects.filter(username__exact = nombre_usuario):
                #   Si el usuario no existe lo agregamos   
                print "Agregando usuario %s" % nombre_usuario
                u = User.objects.create_user(
                    username = nombre_usuario,
                    email = data['nuevo_correo'],
                )
                u.set_password(data['nueva_password'])
                u.first_name = data['nuevo_nombre']
                u.last_name = data['nuevo_apellido']
                u.save()
    
                #   Creamos un UserProfile asociado al usuario que acabamos de crear
                datos_perfil = {}
                datos_perfil['telefono'] = data['nuevo_telefono']
                #   En caso de agregar algun dato extra al perfil se agregan aqui   
                UserProfile.objects.crear_colaborador(u, datos_perfil)
            else:
                #   Ya habia un usuario registrado con ese nombre de usuario   
                #   raise ValidationError(u'Ya existe')
                pass
            #Redirigir a pagina de creacion correcta de usuario
            lista = User.objects.all()
            puede_eliminar = request.user.has_perm('auth.delete_user')
            puede_modificar = request.user.has_perm('auth.change_user')
            puede_crear = request.user.has_perm('auth.create_user')
            return render(request, 'app_usuarios/lista_usuarios.html', {
                'lista' : lista,
                'puede_eliminar' : puede_eliminar,
                'puede_modificar' : puede_modificar,
                'puede_crear' : puede_crear,
            }, )
        else:
            #   Aqui se deben levantar los errores cuando los datos proporcionados no sean validos
            print "No se pudo crear el usuario"
            return render(request, 'app_usuarios/crear_usuario.html',{ 'form': form, })
    
    else:
        #   Se intento acceder usando un metodo distinto al POST
        form = CrearUsuarioForm()  # Un Form Unbound

        return render(request, 'app_usuarios/crear_usuario.html', { 'form': form, })

@login_required
def listar_usuarios(request):
    """
    Metodo para popular la lista de usuarios que se le mostrara al usuario
    In: request
    Out: vista con lista de usuarios
    Autor: German Leon
    Fecha: 5-11-12
    """
    # Se omite el usuario actual de la lista
    lista = User.objects.exclude(username = request.user.username)
    puede_eliminar = request.user.has_perm('auth.delete_user')
    puede_modificar = request.user.has_perm('auth.change_user')
    puede_crear = request.user.has_perm('auth.create_user')
    return render(request, 'app_usuarios/lista_usuarios.html', {
        'lista' : lista,
        'puede_eliminar' : puede_eliminar,
        'puede_modificar' : puede_modificar,
        'puede_crear' : puede_crear,
    }, )

@login_required
@permission_required('auth.can_change_user')
def modificar_usuario(request):
    """
    Metodo que llama al Manejador de Usuarios para modificar los datos de un usuario
    In: request
    Out: vista para modificar usuario
    Autor: German Leon
    Fecha: 5-11-12
    """
    if request.method == 'POST':

        form = ModificarUsuarioForm(request.POST)
        if form.is_valid():
            print "Modificando la data recibida del formulario"
            data = form.cleaned_data
            nombre_usuario = request.POST['nombre_usuario']
            nombre = data['nombre']
            apellido = data['apellido']
            correo = data['correo']
            #   Datos del UserProfile   
            telefono = data['telefono']
    
            UserProfile.objects.modificar(nombre_usuario, nombre, apellido, telefono, correo)
        else:
            #   Aqui se deben levantar los errores cuando los datos proporcionados no sean validos
            print "No se pudo modificar el usuario"
            print form.errors
            lista = []
            nombre_usuario = request.POST['nombre_usuario']
            lista.append(request.POST['nombre'])
            lista.append(request.POST['apellido'])
            lista.append(request.POST['correo'])
            lista.append(request.POST['telefono'])
            return render(request, 'app_usuarios/modificar_usuario.html', { 'nombre_usuario': nombre_usuario, 'lista': lista, })

    # Se debe excluir de la lista de todos los usuarios el
    # usuario actual
    lista = User.objects.exclude(username = request.user.username)
    puede_eliminar = request.user.has_perm('auth.delete_user')
    puede_modificar = request.user.has_perm('auth.change_user')
    puede_crear = request.user.has_perm('auth.add_user')
    return render(request, 'app_usuarios/lista_usuarios.html', {
        'lista' : lista,
        'puede_eliminar' : puede_eliminar,
        'puede_modificar' : puede_modificar,
        'puede_crear' : puede_crear,
    }, )

    return render(request, 'app_usuarios/lista_usuarios.html', { 'lista' : lista, }, )

@login_required
@permission_required('auth.can_change_user')
def modificar_form(request):
    """
    Metodo que carga el form del usuario que se selecciono para modificarse
    Autor: German Leon
    Fecha: 5-11-12 Version 1.0
    """
    lista = []
    if request.method == 'POST':
        nombre_usuario = request.POST['nombre_usuario']
        lista.append(request.POST['nombre'])
        lista.append(request.POST['apellido'])
        lista.append(request.POST['correo'])
        lista.append(User.objects.get(username=nombre_usuario).get_profile().telefono)
        return render(request, 'app_usuarios/modificar_usuario.html', { 'nombre_usuario' : nombre_usuario, 'lista' : lista })
    listar_usuarios(request)
    return render(request, 'app_usuarios/lista_usuarios.html', { 'lista' : lista, }, )

@login_required
def eliminar_usuario(request):
    """
    Metodo que elimina un usuario de la base de datos
    Nota: Accion solo permitida para cuentas de administradores
    In: request 
    Out: vista listar usuarios
    Autor: German Leon
    Fecha: 5-11-12 Version 1.0
    """
    if request.method == 'POST':
        #   Eliminamos el usuario que se selecciono
        #form = EliminarUsuarioForm(request.POST)
        nombre_usuario = request.POST['nombre_usuario']
        print "Eliminando a %s" % nombre_usuario
        usuario = User.objects.filter(username=nombre_usuario)
        #usuario.update(is_active = False)
        usuario.delete()
        print "Usuario eliminado"

    lista = User.objects.all()
    puede_eliminar = request.user.has_perm('auth.delete_user')
    puede_modificar = request.user.has_perm('auth.change_user')
    puede_crear = request.user.has_perm('auth.create_user')
    return render(request, 'app_usuarios/lista_usuarios.html', {
        'lista' : lista,
        'puede_eliminar' : puede_eliminar,
        'puede_modificar' : puede_modificar,
        'puede_crear' : puede_crear,
    }, )

@login_required
def modificar_perfil(request):
    """
    Metodo para modificar los datos de un usuario ya registrado en el sistema
    In: request
    Out: vista modificar usuario
    Autor: German Leon
    Fecha: 7-11-12 Version 1.0
    """
    usuario = request.user
    nombre_usuario = usuario.username
    perfil_usuario = UserProfile.objects.get(user=usuario)
    lista = []
    lista.append(usuario.first_name)
    lista.append(usuario.last_name)
    lista.append(usuario.email)
    lista.append(perfil_usuario.telefono)
    return render(request, 'app_usuarios/modificar_usuario.html', { 'nombre_usuario' : nombre_usuario, 'lista' : lista })

def logout_view(request):
    """
    Metodo llamado cuando se quiere cerrar la sesion, crea un formulario unbound para el login
    y cierra la sesion del usuario
    In: request
    Out: vista del login
    Autor: German Leon
    Fecha 5-11-12 Version 1.0
    """
    form = LoginForm()
    logout(request)
    return render(request, 'app_usuarios/login.html', { 'form': form, })

def registrar_visitante(request):
    """
    Metodo para crear un usuario con los datos debidamente validados 
    proporcionados por el usuario
    In: request
    Out: vista de registrar visitante
    Autor: German Leon
    Fecha 5-11-12 Version 1.0
    """
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            nombre_usuario = data['nuevo_nombre_usuario']
   
            if not User.objects.filter(username__exact = nombre_usuario):
                #   Si el usuario no existe lo agregamos   
                print "Agregando usuario %s" % nombre_usuario
                u = User.objects.create_user(
                    username = nombre_usuario,
                    email = data['nuevo_correo'],
                )
                u.set_password(data['nueva_password'])
                u.first_name = data['nuevo_nombre']
                u.last_name = data['nuevo_apellido']
                u.save()
    
                #   Creamos un UserProfile asociado al usuario que acabamos de crear
                datos_perfil = {}
                datos_perfil['telefono'] = data['nuevo_telefono']
                #   En caso de agregar algun dato extra al perfil se agregan aqui   
                UserProfile.objects.crear_colaborador(u, datos_perfil)
            else:
                #   Ya habia un usuario registrado con ese nombre de usuario   
                #   raise ValidationError(u'Ya existe')
                pass
            #Redirigir a pagina de creacion correcta de usuario
            form = LoginForm()  
            return render(request, 'app_usuarios/login.html', { 'form': form, })
        else:
            #   Aqui se deben levantar los errores cuando los datos proporcionados no sean validos
            print "No se pudo crear el usuario"
            return render(request, 'app_usuarios/registrar_visitante.html',{ 'form': form, })
    
    else:
        #   Se intento acceder usando un metodo distinto al POST
        form = CrearUsuarioForm()  # Un Form Unbound

        return render(request, 'app_usuarios/registrar_visitante.html', { 'form': form, })

@csrf_exempt
@login_required
def cambiar_contrasena(request):
    """
    Metodo que permite cambiar la contrasena de un usuario 
    In: request 
    Out: vista de cambiar contrasena
    Autor: German Leon
    Fecha 5-11-12 Version 1.0
    """
    if request.method == 'POST':
        form = CambiarContrasenaForm(request.POST)
        if form.is_valid():
            #   Cambiando la contrasena   
            data = form.cleaned_data
            contrasena = data['contrasena1']
            usuario = request.user
            print usuario.email
            usuario.set_password(contrasena)
            usuario.save()

            lista = app_pizarras.views.obtener_pizarras(request)
            return render(request, 'app_pizarras/listar.html', { 'lista' : lista, })
    else:
        form = CambiarContrasenaForm()
    return render(request, 'app_usuarios/cambiar_contrasena.html', { 'form': form, })
