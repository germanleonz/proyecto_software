import datetime
from django.http import HttpResponse
from app_log.models import ManejadorAccion, Accion


class ManejadorLogs():

	#se llama SIEMPREEEE
	def process_response(self, request, response):
		status = response.status_code
#		usuario = request.user

#		if usuario.is_authenticated():
#			if status >= 500:
#				Accion.objects.crearAccion(
#					request.user,
#					"Error interno del servidor",
#					'f')
		return response

