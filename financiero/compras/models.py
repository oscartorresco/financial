from django.db import models
from inventario.models import Producto

#Modelo de Proveedor
class Proveedor(models.Model):
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
class Compra(models.Model):
	codigo = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=100,null=False)
	fecha = models.DateField(null=False)
	proveedor = models.ForeignKey(Proveedor)
	def natural_key(self):
		return (self.descripcion, self.fecha) + (self.proveedor.natural_key(),)
	natural_key.dependencies = ['compras.proveedor']
	def __unicode__(self):
		return self.descripcion

#Modelo de Compra_Producto
class Compra_Producto(models.Model):
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