from django.conf.urls import patterns, url
from compras import views

urlpatterns = patterns('',
	#urls de compras
	url(r'^$', views.indexCompras, name="indexCompras"),
    url(r'^agregar/$', views.agregarCompra, name="agregarCompra"),
    url(r'^listaProductos/$', views.buscarProductos, name="listaProductos"),
    url(r'^listadoCompras/$', views.listadoCompras, name="listadoCompras"),
    url(r'^buscar/$', views.buscarCompra, name="buscarCompra"),
	
    #urls de proveedor
    url(r'^proveedor/$', views.indexProveedor, name="indexProveedor"),
    url(r'^proveedor/agregar/$', views.agregarProveedor, name="agregarProveedor"),
    url(r'^proveedor/buscar/$', views.buscarProveedor, name="buscarProveedor"),
    url(r'^proveedor/buscarPrecio/$', views.buscarPrecioProductoProveedor, name="buscarPrecio"),
    url(r'^proveedor/editar/$', views.editarProveedor, name="editarProveedor"),

    #url(r'^(?P<codigo_proveedor>\d+)/$', views.detalle, name="detalleProveedor"),
)