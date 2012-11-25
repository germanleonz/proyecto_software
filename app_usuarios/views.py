import re
import app_pizarras
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import views as views_admin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

from app_usuarios.models import *
from app_usuarios.forms import LoginForm, CrearUsuarioForm, ModificarUsuarioForm

def login_usuario(request):
    """	
    Metodo que verificar las credenciales del usuario y permite o no el acceso
    sistema
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
                    login(request, usuario)
                    print "Acceso permitido para %s" % nombre_usuario
                    #   Redirigir a pagina de login correcto (ver pared)
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

@csrf_exempt
@login_required
@permission_required('auth.create_user')
def crear_usuario(request):
    """
    Metodo para crear un usuario con los datos debidamente validados 
    proporcionados por el usuario
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
                crear_colaborador(u, datos_perfil)
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
    """
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
@permission_required('auth.can_change_user')
def modificar_usuario(request):
    """
    Metodo que llama al Manejador de Usuarios para modificar los datos de un usuario
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
    
            modificar(nombre_usuario, nombre, apellido, telefono, correo)
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

    lista = User.objects.all()
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
    dostring de modificar_form
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

def invitar_usuario(request):
    """
    Metodo que invita a un colaborador a hacerse responsable de una actividad
    parametros: id_actividad a la que se le esta asignando un responsable y correo 
    de la persona a la que se le esta asignando 
    """
    if request.method == 'POST':
        id_actividad = request.post['id_actividad']
        recipiente = request.post['recipiente']
        remitente = "pizarras@software.com"
        if UserProfile.getEmail():
            #   El usuario ya esta registrado le enviamos un correo
            nombre_usuario = recipiente.partition("@")[0]  
            contrasena = User.object.make_random_password()
            asunto = "Felicidades, usted ha sido invitado a participar como colaborador"
            mensaje = """
                Felicidades usted ha sido invitado a trabajar como colaborador en un actividad 
                Su nombre de usuario es: {0} 
                Su contrasena es: {1}

                Por su seguridad le recomendamos cambiar la clave tan pronto como le sea posible
            """.format(unicode(usuario), unicode(contrasena))
            send_mail(asunto, mensaje, remitente, [recipiente],  fail_silently = False)

            #   Creamos el usuario con nombre de usuario y contrasena como unicos datos
            User.objects.create(username=nombre_usuario)
            datos = {}
            datos['telefono'] = ""
            crear_colaborador(usuario, datos)
        else:

        #   Llamar a algun metodo de la app_actividad que se encargue de asignarle la actividad
        #   al usuario recien creado
    lista = app_pizarras.views.obtener_pizarras(request)
    return render(request, 'app_pizarras/listar.html', { 'lista' : lista, }) #  Esta vista puede ser cualquier otra  

def logout_view(request):
    """
    Metodo llamado cuando se quiere cerrar la sesion, crea un formulario unbound para el login
    y cierra la sesion del usuario
    """
    form = LoginForm()
    logout(request)
    return render(request, 'app_usuarios/login.html', { 'form': form, })

def registrar_visitante(request):
    """
    Metodo para crear un usuario con los datos debidamente validados 
    proporcionados por el usuario
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
                crear_colaborador(u, datos_perfil)
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

