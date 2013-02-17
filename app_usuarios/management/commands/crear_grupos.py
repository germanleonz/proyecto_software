from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    args = "<Ningunos>"
    help = "Crea los grupos de administradores y colaboradores y les asigna permissions"

    def handle(self, *args, **options):
        print "Creando grupos de colaboradores y administradores..."

        #   Creamos los grupos  de colaboradores y administradores
        print "Creando grupos ..."
        colaboradores, colab_creados = Group.objects.get_or_create(name="Colaboradores")
        administradores, admin_creados = Group.objects.get_or_create(name="Administradores")
        print "Listo"

        print "Agregando permisos ..."
        #   Agregamos permisos de gestion de usuarios a los administradores
        administradores.permissions.add(Permission.objects.get(codename="add_user"))
        administradores.permissions.add(Permission.objects.get(codename="add_userprofile"))
        administradores.permissions.add(Permission.objects.get(codename="delete_user"))
        administradores.permissions.add(Permission.objects.get(codename="delete_userprofile"))
        administradores.permissions.add(Permission.objects.get(codename="change_user"))
        administradores.permissions.add(Permission.objects.get(codename="change_userprofile"))

        #   Agregamos permisos de gestion de pizarras y actividades

        print "Listo"

