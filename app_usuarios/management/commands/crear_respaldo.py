from django.core.management.base import BaseCommand, CommandError

import subprocess
import tarfile
import os

dirname = os.path.dirname
PROJECT_PATH = os.path.realpath(dirname(dirname(dirname(dirname(__file__)))))

def respaldar_BD():
    """ Crea un respaldo de la base de datos del sistema  """
    host_bd = "localhost"
    usuario_bd = "postgres"
    nombre_bd = "proyecto_pizarra"
    nombre_respaldo_bd = "respaldo_bd.txt"

    print "Respaldando la base de datos ..."
    comando_respaldo_bd = "pg_dump -h {0} -U {1} -f {2} {3}".format(
            host_bd, usuario_bd, nombre_respaldo_bd, nombre_bd)
    subprocess.Popen(comando_respaldo_bd, shell=True)
    print "Listo"
    
def respaldar_codigo():
    """ Crea un respaldo del codigo fuente del sistema  """
    print "Respaldando codigo fuente ..."
    archivos = ['app_actividad', 'app_comentarios', 'app_log',
            'app_pizarras', 'app_usuarios', 'config', 'manage.py',
            'middleware', 'proyecto_pizarras', 'README.md', 'respaldo_bd.txt',
            'static', 'templates']
    nombre_tar = "respaldo_codigo.tar.gz"
    tar = tarfile.open(nombre_tar, "w:gz")
    for name in archivos:
        tar.add(name)
    tar.close()
    print "Listo"

class Command(BaseCommand):
    """ Este script respalda la base de datos y el codigo fuente del sistema """
    args = "<Ningunos>"
    help = "Comando que ejecuta un respaldo de la base de datos y del codigo fuente"

    def handle(self, *args, **options):
        os.chdir(PROJECT_PATH)
        respaldar_BD()
        respaldar_codigo()
