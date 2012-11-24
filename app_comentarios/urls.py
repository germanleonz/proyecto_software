from django.conf.urls import patterns, url
from app_comentarios import views

urlpatterns = patterns('',
  url(r'^crear_comentario/',views.crear_comentario, name='crear_comentario'),
  url(r'^eliminar_comentario/',views.eliminar_comentario, name='eliminar_comentario'),
)

