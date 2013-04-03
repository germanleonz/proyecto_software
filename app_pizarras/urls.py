from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from app_pizarras import views
from app_pizarras import rest_views

urlpatterns = patterns('',
        url(r'^crear_pizarra/',views.crear_pizarra, name='crear_pizarra'),
        url(r'^listar_pizarra/',views.listar_pizarra, name='listar_pizarra'),
        url(r'^modificar_pizarra/',views.modificar_pizarra, name='modificar_pizarra'),
        url(r'^modificar_form/',views.generar_form_modificar, name='modificar_form'),
        url(r'^eliminar_pizarra/',views.eliminar_pizarra, name='eliminar_pizarra'),
        url(r'^visualizar_pizarra/',views.visualizar_pizarra, name='visualizar_pizarra'),
        url(r'^orden_cronologico/',views.vista_orden_cronologico, name='orden_cronologico'),
        url(r'^orden_estados/',views.vista_orden_estados, name='orden_estados'),
        url(r'^orden_avance/',views.vista_orden_avance, name='orden_avance'),
        url(r'^listar_pizarras_rest/$', rest_views.PizarraList.as_view(), name='listar_pizarra_rest'),
        url(r'^rest_pizarras_usuario/(?P<username>[\w]+)/$', rest_views.PizarraList.as_view(), name='pizarras_usuarios_rest'),
        url(r'^rest/(?P<pk>[0-9]+)/$', rest_views.PizarraDetail.as_view(), name='rest_pizarra_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
