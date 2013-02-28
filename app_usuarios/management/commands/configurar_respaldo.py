from django.core.management.base import BaseCommand, CommandError
from crontab import CronTab

import os
import getpass

class Command(BaseCommand):
    """docstring for Command"""
    args = "<Ningunos>"
    help = "Comando para configurar los respaldos automaticos del sistema"

    def handle(self, *args, **options):
        #   Variables correspondientes al respaldo
        minutos = 1
        horas = 19
        dia = 3
        meses = 02

        self.stdout.write("Configuracion de respaldos automaticos del proyecto pizarra ...\n")
        usuario = getpass.getuser()
        cron = CronTab(usuario)

        cron.remove_all('manage.py')

        job = cron.new(command="{0}/{1} > /tmp/output.txt".format(os.getcwd(), 'manage.py crear_respaldo'))

        #   Configuracion de la frecuencia de respaldos
        job.minute.every(minutos)
        #job.hour.on(horas)
        #job.dow.on(dia)
        #job.dom.on(dia)
        #job.month.on(meses)

        #   Finalmente se guardan los cambios
        cron.write()
        self.stdout.write("Configuracion terminada\n")
