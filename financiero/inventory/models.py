#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class  Bodega(models.Model):
	codigo = models.AutoField(max_length=30, primary_key=True)
	nombre = models.CharField(max_length=30)
	direccion = models.CharField(max_length=50)
	def __unicode__(self):
		return self.nombre

class  Producto(models.Model):
	codigo = models.AutoField(max_length=30, primary_key=True)
	nombre = models.CharField(max_length=30)
	descripcion = models.CharField(max_length=50)
	medida  = models.CharField(max_length=30)
	inventario_minimo = models.IntegerField(max_length=30)
	cantidad = models.IntegerField(max_length=30)
	fecha_ingreso = models.DateField(auto_now=False)
	imagen = models.ImageField(upload_to='financial', verbose_name='Imágen')
	bodega =models.ForeignKey(Bodega)
	def __unicode__(self):
		return self.bodega

