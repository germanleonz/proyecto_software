import re
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.utils.encoding import smart_str
from django.core.exceptions import ValidationError

def crear_colaborador(usuario, datos):
    """
    Manejador para la senal creacion_usuario
    """
    print "Entramos a crear_colaborador"
    up = UserProfile.objects.create(user=usuario, telefono= datos["telefono"])
    #   Agregamos el usuario recien creado al grupo de los colaboradores
    usuario.groups.add(Group.objects.get(name="Colaboradores"))

def crear_administador(usuario, datos):
    """
    Metodo para crear un Administrador
    """
    #   Creamos un usuario como en crear_colaborador pero con privilegios de administador
    print "Asignandole privilegios de administrador al usuario recien creado ..."
    crear_colaborador(usuario, datos)
    #   Agregamos al usuario recien creado al grupo de administradores
    usuario.groups.add(Group.objects.get(name="Administradores"))

class UserProfile(models.Model):
    """
    Clase UserProfile que extiende los datos que se definen en la tabla User de Django
    Nota: Deprecado esta manera de extender User esta deprecada en Django 1.5
    """
    #   Campo obligatorio para poder extender
    user = models.OneToOneField(User)
    #   Campos adicionales
    telefono = models.CharField(max_length=15)
    
    def save(self, *args, **kwargs):
        self.telefono = smart_str(self.telefono, encoding="utf-8")
        if re.match('^[0-9]+[-]?[0-9]+$', self.telefono) == None:
            raise ValidationError(u'\"%s\" Error. El telefono solo puede estar compuesto por numeros' % self.telefono)
        else:    
        	super(UserProfile,self).save(*args,**kwargs)


    def __unicode__(self):
        return self.user.username + ", " + self.telefono


def modificar(nombre_usuario, nombre, apellido, telefono, correo):
    """
    Metodo para actualizar los datos de un User incluyendo los datos 
    de su UserProfile
    """
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
