from django.conf.urls import patterns, url
from app_actividad import views

urlpatterns = patterns('',
        url(r'^crear_actividad/',views.crear_actividad, name='crear_actividad'),
        url(r'^listar_actividad/',views.listar_actividad, name='listar_actividad'),
        url(r'^modificar_actividad/',views.modificar_actividad, name='modificar_actividad'),
        url(r'^eliminar_actividad/',views.eliminar_actividad, name='eliminar_actividad'),
        url(r'^visualizar_actividad/',views.visualizar_actividad, name='visualizar_actividad'),
        url(r'^modificar_form/',views.generar_form_modificar, name='modificar_form'),
        url(r'^cambiar_estado_actividad/',views.cambiar_estado_actividad, name='cambiar_estado_actividad'),
        url(r'^form_crear/',views.form_crear, name='form_crear'),
)

