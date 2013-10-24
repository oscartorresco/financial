from django.db import models

class Persona(models.Model):
	documento=models.BigIntegerField(primary_key=True, null=False)
	nombres= models.CharField(max_length=50, null=False)
	apellidos= models.CharField(max_length=50, null=False)
	direccion= models.CharField(max_length=50, null=False)
	telefono1= models.CharField(max_length=50, null=False)
	telefono2= models.CharField(max_length=50)
	hojaVida= models.FileField(upload_to="docs/")
	def __unicode__ (self):
		return self.nombres+' '+self.apellidos

