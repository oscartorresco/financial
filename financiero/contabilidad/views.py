# Create your views here.
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from contabilidad.models import PUC, Transaccion

def contabilidad(request):
    listaTransacciones = Transaccion.objects.filter(tipo=0)
    listaPUC= PUC.objects.all()
    context = {'transacciones': listaTransacciones, 'cuenta': listaPUC}
    return render(request,'contabilidad/cuentasPorPagar.html',context)

def crearTransaccion(request):
    if request.method == 'POST':
        cuenta= request.POST['cuenta']
        concepto= request.POST['concepto']
        fecha= request.POST['fecha']
        valor= request.POST['valor']
        tipo= '0'
        #Falta Corregir errores de ingreso
        transaccion = Transaccion(0,cuenta,concepto,valor,fecha,tipo)
        transaccion.save()
        return redirect('contabilidad.views.contabilidad')
        