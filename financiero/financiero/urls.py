from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'financiero.views.home', name='home'),
    # url(r'^financiero/', include('financiero.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^$', 'main.home'), #URL a la pagina principal del subsitema financiero

    url(r'^ventas/', include('sells.urls')),    
    url(r'^compras/', include('compras.urls')),
    url(r'^contabilidad/', include('contabilidad.urls')),


)
