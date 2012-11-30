from django.conf.urls import patterns, url

from app_log import views as views_log
from django.contrib.auth import views as views_admin

urlpatterns = patterns('',
    url(r'^consultar_log/', views_log.visualizar_accion_user, name='visualizar_log_user'),
)
