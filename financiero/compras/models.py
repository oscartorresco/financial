from django.db import models

# Create your models here.
class Bodega(models.Model):
	codigo = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=100,null=False)
	direccion = models.CharField(max_length=100,null=False)
	def __unicode__(self):
		return self.nombre+' Ubicada en '+self.direccion

class Compra(models.Model):
	codigo = models.IntegerField(primary_key=True)
	descripcion = models.CharField(max_length=100,null=False)
	fecha = models.DateField(null=False)
	def __unicode__(self):
		return self.descripcion

class Producto(models.Model):
    codigo = models.IntegerField(primary_key=True, null=False)
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=300, null=False)
    UNIDADES_MEDIDA =(
    		('Unidad', 'Unidad'),
    		('Decena', 'Decenas'),
    		('Docena', 'Docenas'),
    		('Kg','Kilogramo'),
    		('gr','Gramo'),
    		('m','Metro')
    	)
    medida = models.CharField(max_length=30, null=False, choices=UNIDADES_MEDIDA)
    inventario_minimo = models.IntegerField(null=False)
    cantidad = models.IntegerField(null=False)
    fecha_ingreso = models.DateField(null=False)
    bodega = models.ForeignKey(Bodega)
    def __unicode__(self):
		return self.nombre

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