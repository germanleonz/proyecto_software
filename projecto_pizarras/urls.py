from django.conf.urls import patterns, include, url
from app_usuarios import views as views_usuarios
from app_usuarios.models import UserProfile
from app_usuarios.models import UserProfile
from app_pizarras.models import Pizarra
from app_comentarios.models import Comentario
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app_actividad.models import Actividad
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

admin.site.register(UserProfile)
admin.site.register(Pizarra)
admin.site.register(Actividad)
admin.site.register(Comentario)
admin.autodiscover()
dajaxice_autodiscover()
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^$', views_usuarios.login_usuario, name='login_usuario'),
    url(r'^usuarios/', include('app_usuarios.urls', namespace="app_usuarios")),
    url(r'^pizarras/', include('app_pizarras.urls', namespace="app_pizarras")),
    url(r'^actividad/', include('app_actividad.urls', namespace="app_actividad")),
    url(r'^comentarios/', include('app_comentarios.urls', namespace="app_comentarios")),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += staticfiles_urlpatterns()
