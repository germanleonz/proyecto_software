from django.dispatch import Signal
creacion_usuario = Signal(providing_args=["instance", "telefono", "rol"])
