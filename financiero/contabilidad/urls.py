from django.conf.urls import patterns, url
from contabilidad import views

urlpatterns = patterns('',
    #urls de compras
    url(r'^$', views.contabilidad, name="contabilidad"),
    url(r'^agregar/$', views.crearTransaccion, name="crearTransaccion"),
)