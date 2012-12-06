import re
import datetime
from django.db import models
from django.contrib.auth.models import User, Group, Permission, UserManager
from django.utils.encoding import smart_str
from django.core.exceptions import ValidationError
from app_log.models import ManejadorAccion, Accion

class ManejadorUsuario(UserManager):
    def crear_colaborador(self, data, usuario):
        """
        Crea un colaborador con los datos proporcionados
        In: self, usuario, datos
        Out: --
        Autor: German Leon
        Fecha: 4-11-12 Version 1.0
        """
        print "Entramos a crear_colaborador"
        u = User.objects.create_user(
            username = data['nuevo_nombre_usuario'],
            email = data['nuevo_correo'],
        )
        u.set_password(data['nueva_password'])
        u.first_name = data['nuevo_nombre']
        u.last_name = data['nuevo_apellido']
        u.save()

        up = UserProfile.objects.create(user=u, telefono= data["nuevo_telefono"])
        #   Agregamos el usuario recien creado al grupo de los colaboradores
        u.groups.add(Group.objects.get(name="Colaboradores"))


        #Se registra en el log que "usuario" creo a un nuevo colaborador
        fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        Accion.objects.crearAccion(
            u, 
            "El usuario %s agrego a %s" % (usuario.username, u.first_name),
            fechaYHora,
            'i')  

    def crear_administador(self, usuario, datos):
        """
        Metodo para crear un Administrador
        In: self, usuario, datos
        Out: --
        Autor: German Leon
        Fecha: 4-11-12 Version 1.0
        """
        #   Creamos un usuario como en crear_colaborador pero con privilegios de administador
        print "Asignandole privilegios de administrador al usuario recien creado ..."
        crear_colaborador(self, datos, usuario)
        #   Agregamos al usuario recien creado al grupo de administradores
        usuario.groups.add(Group.objects.get(name="Administradores"))

    def modificar(self, nombre_usuario, nombre, apellido, telefono, correo, usuario):
        """
        Crea un administrador con sus respectivos permisos
        In: self, nombre_usuario, nombre, apellido, telefono, correo 
        Out: --
        Autor: German Leon
        Fecha: 4-11-12 Version 1.0
        """
        modificado = User.objects.get(username = nombre_usuario)
        nuevo = User.objects.filter(username = nombre_usuario)
        nuevoProfile = UserProfile.objects.filter(user=nuevo)
        nombreB = False
        apellidoB = False
        telefonoB = False
        correoB = False
        if nombre == "":
            nombreB = True
        if apellido == "":
            apellidoB = True
        if correo == "":
            correoB = True
        if telefono == "":
            telefonoB = True

        if not nombreB and not apellidoB and not correoB and not telefonoB:
            nuevo.update(first_name=nombre, last_name= apellido, email = correo)
            nuevouser = nuevoProfile.get()
            nuevouser.telefono = telefono
            nuevouser.save()
            print nuevoProfile.values()

            #Se agrega en el log que "usuario" edito su perfil

            fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            #si el usuario esta modificando su propio perfil
            if (usuario.username == modificado.username):
                Accion.objects.crearAccion(
                    usuario,
                    "El usuario %s modifico la informacion de su perfil" % usuario.username,
                    fechaYHora,
                    'i')
            else:
                Accion.objects.crearAccion(
                usuario,
                "El usuario %s modifico la informacion de %s" % (usuario.username, modificado.username),
                fechaYHora,
                'i')


    def eliminar(self, nombre_usuario, nombre_userloggeado):
        usuario = User.objects.get(username=nombre_usuario)
        usuario.is_active = False
        usuario.save()

        #si se intenta eliminar a un usuario que es administrador se considera
        #a ese log como warning, si se elimina a un colaborador el log es de tipo info.
        fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if usuario.groups.filter(name='Administradores').exists():
            Accion.objects.crearAccion(
                usuario,
                "El usuario %s elimino al administrador %s" % (nombre_userloggeado, nombre_usuario),
                fechaYHora,
                'w')
        else:            
            Accion.objects.crearAccion(
                usuario,
                "El usuario %s elimino a %s" % (nombre_userloggeado, nombre_usuario),
                fechaYHora,
                'i')


class UserProfile(models.Model):
    """
    Clase UserProfile que extiende los datos que se definen en la tabla User de Django
    Nota: Deprecado esta manera de extender User esta deprecada en Django 1.5
    Autor: German Leon
    Fecha: 4-11-12 Version 1.0
    """
    #   Campo obligatorio para poder extender
    user = models.OneToOneField(User)
    #   Campos adicionales
    telefono = models.CharField(max_length=15)

    #   El Manager de UserProfile sera el ManejadorUsuario que definimos
    objects = ManejadorUsuario()
    
    def save(self, *args, **kwargs):
        self.telefono = smart_str(self.telefono, encoding="utf-8")
        if re.match('^[0-9]+[-]?[0-9]+$', self.telefono) == None:
            raise ValidationError(u'\"%s\" Error. El telefono solo puede estar compuesto por numeros' % self.telefono)
        else:    
        	super(UserProfile,self).save(*args,**kwargs)

    def __unicode__(self):
        return self.user.username + ", " + self.telefono
