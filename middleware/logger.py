import datetime
from django.http import HttpResponse
from app_log.models import ManejadorAccion, Accion


class ManejadorLogs():
	# c = 0
	# #se llama justo antes de que Django llame a una vista
	# def process_view(self, request, view_func, view_args, view_kwargs):
	# 	print "\nPROCESS VIEW"
	# 	status = HttpResponse.status_code
	# 	print "en view---- " + str(status)

	# 	return None

	# #se llama cuando en un views se produce una excepcion
	# def process_exception(self, request, exception):
	# 	print "\nProcess exception"

	# 	print type(exception), exception.message
	# 	return None

	#se llama SIEMPREEEE
	def process_response(self, request, response):
		status = response.status_code
		fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		return response
                """ if request.user:
		    usuario = request.user
                    if usuario.is_authenticated():
                        if status >= 500:
                                Accion.objects.crearAccion(
                                        request.user,
                                        "Error interno del servidor",
                                        fechaYHora,
                                        'f') 
                """
