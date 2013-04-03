from django.conf.urls import patterns, url
from django.contrib.auth import views as views_admin

from rest_framework.urlpatterns import format_suffix_patterns

from app_usuarios import views as views_usuarios
from app_usuarios import rest_views as rest_views_usuarios

urlpatterns = patterns('',
    url(r'^crear_usuario/', views_usuarios.crear_usuario, name='crear_usuario'),
    url(r'^registrar_visitante/', views_usuarios.registrar_visitante, name='registrar_visitante'),
    url(r'^cambiar_contrasena/', views_usuarios.cambiar_contrasena, name='cambiar_contrasena'),
    url(r'^listar_usuarios/', views_usuarios.listar_usuarios, name='listar_usuarios'),
    url(r'^modificar_usuario/', views_usuarios.modificar_usuario, name='modificar_usuario'),
    url(r'^modificar_form/', views_usuarios.modificar_form, name='modificar_form'),
    url(r'^eliminar_usuario/', views_usuarios.eliminar_usuario, name='eliminar_usuario'),
    url(r'^resetpassword/passwordsent/$', views_admin.password_reset_done),
    url(r'^resetpassword/$', views_admin.password_reset, name = "password_reset"),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', views_admin.password_reset_confirm),
    url(r'^reset/done/$', views_admin.password_reset_complete),
    url(r'^cerrar_sesion/', views_usuarios.logout_view, name='logout_view'),
    url(r'^perfil_usuario/',views_usuarios.perfil_usuario, name='perfil_usuario'),
    url(r'^login/(?P<nombre_usuario>\w+)/(?P<clave>[\w\d]+)/$', rest_views_usuarios.Login.as_view(), name='rest_login'),
    url(r'^crear_usuario_rest/', rest_views_usuarios.UserProfileList.as_view(), name='rest_create_user'),
    #url(r'^login/(?P<nombre_usuario>\w+)/(?P<clave>[\w\d]+)/$', rest_views_usuarios.Login.as_view(), name='rest_login'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
