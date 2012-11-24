from django.conf.urls import patterns, url
from app_pizarras import views

urlpatterns = patterns('',
        url(r'^crear_pizarra/',views.crear_pizarra, name='crear_pizarra'),
        url(r'^listar_pizarra/',views.listar_pizarra, name='listar_pizarra'),
        url(r'^modificar_pizarra/',views.modificar_pizarra, name='modificar_pizarra'),
        url(r'^modificar_form/',views.generar_form_modificar, name='modificar_form'),
        url(r'^eliminar_pizarra/',views.eliminar_pizarra, name='eliminar_pizarra'),
        url(r'^visualizar_pizarra/',views.visualizar_pizarra, name='visualizar_pizarra'),
)

