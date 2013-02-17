from django.core.management.base import BaseCommand, CommandError
from crontab import CronTab

import getpass
import subprocess

class Command(BaseCommand):
    """docstring for Command"""
    args = "<Ningunos>"
    help = "Comando para configurar los respaldos automaticos del sistema"

    def handle(self, *args, **options):
        #   Variables correspondientes al respaldo
        minutos = None
        horas = None
        dias = None
        meses = None

        self.stdout.write("Configuracion de respaldos automaticos del proyecto pizarra\n")
        usuario = getpass.getuser()
        cron = CronTab(usuario)
        job = cron.new(command='python manage.py crear_respaldo')
        job.minute.during(5,50).every(5)
        job.hour.every(1)
        #cron.write()
        print "Configuracion terminada"
