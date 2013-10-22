from django.conf.urls import patterns, url
from compras import views

urlpatterns = patterns('',
	#urls de compras
	url(r'^$', views.indexCompras, name="indexCompras"),
    url(r'^agregar/$', views.agregarCompra, name="agregarCompra"),
	
    #urls de proveedor
    url(r'^proveedor/$', views.indexProveedor, name="indexProveedor"),
    url(r'^proveedor/agregar/$', views.agregarProveedor, name="agregarProveedor"),
    url(r'^proveedor/(?P<codigo_proveedor>\d+)/$', views.editarProveedor, name="editarProveedor"),
    url(r'^proveedor/(?P<codigo_proveedor>\d+)/lista/$', views.listaProductosProveedor, name="listaProductosProveedor"),
    url(r'^proveedor/(?P<codigo_proveedor>\d+)/agregarProducto/$', views.agregarProductoProveedor, name="agregarProductoProveedor"),
    #url(r'^(?P<codigo_proveedor>\d+)/$', views.detalle, name="detalleProveedor"),
)