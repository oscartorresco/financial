from django.conf.urls import patterns, include, url



urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'main.views.home'),
    url(r'^nueva_venta/', 'sells.views.nueva_venta'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
