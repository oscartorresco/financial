from django.db import models
from inventario.models import Producto

#Modelo de Proveedor
class ProveedorManager(models.Manager):
	def get_by_natural_key(self, nombre):
		return self.get(nombre = nombre)

class Proveedor(models.Model):
	objects = ProveedorManager()
	codigo = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=100, null=False)
	direccion = models.CharField(max_length=100, null=False)
	telefono = models.CharField(max_length=50, null=False, unique=True)
	estado = models.BooleanField(null=False)
	def __unicode__(self):
		return self.nombre
	def natural_key(self):
		return (self.nombre)
	class Meta:
		unique_together = (('nombre'),)

#Modelo de Compra
class CompraManager(models.Manager):
	def get_by_natural_key(self, proveedor, descripcion):
		return self.get(descripcion=descripcion, proveedor = proveedor)

class Compra(models.Model):
	objects = CompraManager()
	codigo = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=100,null=False)
	fecha = models.DateField(null=False)
	proveedor = models.ForeignKey(Proveedor)
	def natural_key(self):
		return (self.descripcion,) + (self.proveedor.natural_key(),)
	natural_key.dependencies = ['compras.proveedor']
	def __unicode__(self):
		return self.descripcion

#Modelo de Compra_Producto
class CompraProductoManager(models.Manager):
 	def get_by_natural_key(self, compra):
 		return self.get(compra = compra)

class Compra_Producto(models.Model):
	#objects = CompraProductoManager()
	cantidad = models.IntegerField(null=False)
	precio = models.BigIntegerField(null=False)
	compra = models.ForeignKey(Compra)
	producto = models.ForeignKey(Producto)
	def natural_key(self):
		return (self.compra)
	natural_key.dependencies = ['compras.compra']

#Modelo de Compra Producto_Proveedor
class Producto_Proveedor(models.Model):
	precio_oferta = models.BigIntegerField(null=False)
	proveedor = models.ForeignKey(Proveedor)
	producto = models.ForeignKey(Producto)
	def __unicode__(self):
		return str(self.producto) + " ofrecido por " + str(self.proveedor)