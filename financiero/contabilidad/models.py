from django.db import models
'''
Teniendo en cuenta que en el PUC de acuerdo al numero de digitos se define si
es una CLASE(1), GRUPO(2), CUENTA(4) Y SUBCUENTA(6) se define simplemente una
tabla que posea el catalogo de cuentas del PUC donde la respectiva clasificacion se hace mediante la capa
de logica
''' 
class PUC(models.Model):
    codigo= models.IntegerField(primary_key=True)
    nombre= models.CharField(max_length=100,null=False)
    NATURALEZA_CUENTA=(
            ('0','Debito'),
            ('1','Credito')
        )
    naturaleza=models.CharField(max_length=30, null=False, choices=NATURALEZA_CUENTA)
    def __unicode__(self):
        return str(self.codigo)+' - '+self.nombre
    def natural_key(self):
        return str(self.codigo) +' - '+ self.nombre
    
class Transaccion(models.Model):
    id=models.IntegerField(primary_key=True)
    numero_cuenta=models.ForeignKey(PUC)
    concepto= models.CharField(max_length=100,null=False)
    valor=models.IntegerField()
    fecha=models.DateField()
    TIPO_TRANSACCION=(
            ('0','Cuentas_Por_Pagar'),
            ('1','Cuentas_Por_Cobrar'),
            ('2','Bancos')
        ) #En una sola tabla se manejan los 3 libros para la contabilidad basica.
    tipo=models.CharField(max_length=20, null=False, choices=TIPO_TRANSACCION)
    def __unicode__(self):
        return self.concepto+' - '+self.valor
    def natural_key(self):
        return self.numero_cuenta.natural_key()
    natural_key.dependencies = ['contabilidad.PUC']
    
    