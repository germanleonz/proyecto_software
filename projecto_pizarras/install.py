from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from django.contrib.auth.models import User, Group, Permission

#   Creamos los grupos  de colaboradores y administradores
colaboradores = Group.objects.create(name = "Colaboradores")
administradores = Group.objects.create(name = "Administradores")

#   Les agregamos permisos de gestion de usuarios a los administradores
administradores.permissions.add(Permission.objects.get(codename="delete_user"))
administradores.permissions.add(Permission.objects.get(codename="delete_user_profile"))
administradores.permissions.add(Permission.objects.get(codename="change_user"))
administradores.permissions.add(Permission.objects.get(codename="change_userprofile"))



