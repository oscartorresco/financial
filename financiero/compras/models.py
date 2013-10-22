from django.db import models

# Create your models here.
class Compra(models.Model):
	codigo = models.IntegerField(primary_key=True)
	descripcion = models.CharField(max_length=100,null=False)
	fecha = models.DateField(null=False)
	def __unicode__(self):
		return self.descripcion

class Compra_Producto(models.Model):
	cantidad = models.IntegerField(null=False)
	precio = models.BigIntegerField(null=False)
	compra = models.ForeignKey(Compra)
	producto = models.ForeignKey(Producto)
	def __unicode__(self):
		return self.descripcion

class Proveedor(models.Model):
	codigo = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=100, null=False)
	direccion = models.CharField(max_length=100, null=False)
	telefono = models.CharField(max_length=50, null=False)
	estado = models.BooleanField(null=False)
	def __unicode__(self):
		return self.nombre

class Producto_Proveedor(models.Model):
	precio_oferta = models.BigIntegerField(null=False)
	proveedor = models.ForeignKey(Proveedor, null=False)
	producto = models.ForeignKey(Producto,null=False)
	def __unicode__(self):
		return ' ofrecido por '+self.proveedor__nombre
