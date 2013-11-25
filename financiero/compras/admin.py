from compras.models import Compra, Proveedor, Compra_Producto, Producto_Proveedor
from django.contrib import admin 
admin.site.register(Compra)
admin.site.register(Proveedor)
admin.site.register(Producto_Proveedor)
admin.site.register(Compra_Producto)