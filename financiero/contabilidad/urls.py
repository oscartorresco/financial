from django.conf.urls import patterns, url
from contabilidad import views

urlpatterns = patterns('',
    #urls de compras
    url(r'^$', views.contabilidad, name="contabilidad"),
    url(r'^agregar/$', views.crearTransaccion, name="crearTransaccion"),
    url(r'^balances/$', views.balances, name="balances"),
    url(r'^balanceMes/$', views.balanceMes, name="balanceMes"),
)