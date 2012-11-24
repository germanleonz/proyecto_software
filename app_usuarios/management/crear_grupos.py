from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = "<Ningunos>"
    help = "Crea los grupos de administradores y colaboradores y les asigna permissions"

 #   Creamos los grupos  de colaboradores y administradores
administradores = Group(name = "Administradores")
colaboradores = Group(name = "Colaboradores")

#   Les agregamos permisos de gestion de usuarios a los administradores
administradores.permissions.add(Permission.objects.get(codename="delete_user"))
administradores.permissions.add(Permission.objects.get(codename="delete_user_profile"))
administradores.permissions.add(Permission.objects.get(codename="change_user"))
administradores.permissions.add(Permission.objects.get(codename="change_userprofile"))

