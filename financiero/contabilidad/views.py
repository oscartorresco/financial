# Create your views here.
import json
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from contabilidad.models import PUC, Transaccion
from contabilidad.paginator import Paginador
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.db.models import Q
from django.db import connection
from django.db import models
from django.core import serializers
from datetime import datetime
from _mysql_exceptions import Error

def balances(request):
    return render(request,'contabilidad/balances.html')

def balanceMes(request):
    if request.method == 'POST':
        opcion= int(request.POST['opcion'])
        anio= int(request.POST['anio'])
        if opcion == '0' or anio== '0':
            msn= 'Seleccione una opcion Valida'
            context = {'mensaje': msn}
            return render(request,'contabilidad/balances.html',context)
        else:
            #Condicionamos para el caso en que el Balance se realize en enero y los saldos vengan del anio pasado
            
            anio2=anio
            if opcion==1:#Si es Enero
                anio2=anio2-1 #Para saldos anteriores utilize el anio anterior
                opcion2=12
            else:
                opcion2 = opcion-1
            cursor = connection.cursor()
            cursor.execute('(SELECT t.numero_cuenta_id,c.nombre, SUM(t.valor) valor, MONTH(t.fecha) fecha, t.tipo FROM financiero.contabilidad_transaccion t, financiero.contabilidad_puc c WHERE MONTH(fecha)='+str(opcion)+' and YEAR(fecha)='+str(anio)+' AND t.numero_cuenta_id=c.codigo GROUP BY numero_cuenta_id,tipo)UNION(SELECT t.numero_cuenta_id,c.nombre, SUM(t.valor) valor, MONTH(t.fecha) fecha, t.tipo FROM financiero.contabilidad_transaccion t, financiero.contabilidad_puc c WHERE MONTH(fecha)<='+str(opcion2)+' and YEAR(fecha)='+str(anio2)+' AND t.numero_cuenta_id=c.codigo GROUP BY numero_cuenta_id,tipo)ORDER BY nombre, fecha')
            row = cursor.fetchall()
            print '---------------------------------------------->'+str(len(row))
            
            if len(row) != 0:
                #Definimos la fila para pasarla a un objeto
                lista1=[]
                auxiliar=row[0][0]#Empieza con la primera para poder comparar
                anteriorDebito=0
                anteriorCredito=0
                actualDebito=0
                actualCredito=0
                totalCuentas=0
                total=0
                rango=len(row)
                i=0
                n=0
                #Clase de la cuenta
                clase= PUC.objects.get(pk=str(row[0][0])[0:1])
                fila=[clase,'','','','','','']
                lista1.append(fila)
                #Grupo
                grupo= PUC.objects.get(pk=str(row[0][0])[0:2])   
                fila=[grupo,'','','','','','']
                lista1.append(fila)
                #Subgrupo
                subgrupo= PUC.objects.get(pk=str(row[0][0])[0:4])
                fila=[subgrupo,'','','','','','']
                lista1.append(fila)
                while(n<rango and i<rango):
                        #Validamos que Las cuentas pertenezcan a las mismas clasificaciones
                        if auxiliar == row[i][0]:
                            if row[i][4]=='0': #Debito
                                if row[i][3]==opcion:#Actual
                                    actualDebito=row[i][2]
                                else:#Anterior
                                    anteriorDebito=row[i][2]
                            else:#Credito
                                if row[i][3]==opcion:#Actual
                                    actualCredito=row[i][2]
                                else:#Anterior
                                    anteriorCredito=row[i][2]
                            auxiliar=row[i][0]
                            i=i+1
                            if i==(rango):
                                total=(anteriorDebito+actualDebito)-(anteriorCredito+actualCredito)
                                if PUC.objects.get(pk=str(row[i-1][0])[0:1]).naturaleza == '1':
                                    total=total*-1
                                totalCuentas+=total
                                fila=[str(row[i-1][0])+' - '+ row[i-1][1],anteriorDebito,anteriorCredito,actualDebito,actualCredito,total,'']
                                lista1.append(fila) 
                                #El ultimo total de la ultima cuenta
                                fila=['','','','','','',totalCuentas]
                                lista1.append(fila)
                        else:
                            total=(anteriorDebito+actualDebito)-(anteriorCredito+actualCredito)
                            if PUC.objects.get(pk=str(row[i-1][0])[0:1]).naturaleza == '1':
                                total=total*-1
                            fila=[str(row[i-1][0])+' - '+ row[i-1][1],anteriorDebito,anteriorCredito,actualDebito,actualCredito,total,'']
                            lista1.append(fila) 
                            auxiliar=row[i][0]
                            anteriorDebito=0
                            anteriorCredito=0
                            actualDebito=0
                            actualCredito=0
                            #Como cambia de cuenta necesitamos saber si se trata de la misma clasificacion
                            #O toca cambiar agregar encabezados.
                            #Clase es igual
                            if clase == PUC.objects.get(pk=str(row[i][0])[0:1]):
                                #Vamos sumando el total de cada clase para sacar el balance
                                totalCuentas+=total
                                #Grupo Igual
                                if grupo == PUC.objects.get(pk=str(row[i][0])[0:2]):
                                    #Subgrupo Igual
                                    if subgrupo != PUC.objects.get(pk=str(row[i][0])[0:4]):
                                        subgrupo= PUC.objects.get(pk=str(row[i][0])[0:4])
                                        fila=[subgrupo,'','','','','','']
                                        lista1.append(fila)
                                    #Si el subgrupo es igual entonces no se hace nada
                                else:#Grupo diferente
                                    #Grupo
                                    grupo= PUC.objects.get(pk=str(row[i][0])[0:2])   
                                    fila=[grupo,'','','','','','']
                                    lista1.append(fila)
                                    #Subgrupo
                                    subgrupo= PUC.objects.get(pk=str(row[i][0])[0:4])
                                    fila=[subgrupo,'','','','','','']
                                    lista1.append(fila)
                            else:#Clase diferente
                                #Total
                                totalCuentas+=total
                                fila=['','','','','','',totalCuentas]
                                lista1.append(fila)
                                totalCuentas=0
                                #Clase de la cuenta
                                clase= PUC.objects.get(pk=str(row[i][0])[0:1])
                                fila=[clase,'','','','','','']
                                lista1.append(fila)
                                #Grupo
                                grupo= PUC.objects.get(pk=str(row[i][0])[0:2])   
                                fila=[grupo,'','','','','','']
                                lista1.append(fila)
                                #Subgrupo
                                subgrupo= PUC.objects.get(pk=str(row[i][0])[0:4])
                                fila=[subgrupo,'','','','','','']
                                lista1.append(fila)
                            n=n-1
                        n=n+1
                
                context2 = {'lista': lista1,'mes':opcion,'anio':anio}
                return render(request,'contabilidad/balances.html',context2)
            else:
                mensaje={'aviso':'No hay manejo de cuentas en este mes'}
                return render(request,'contabilidad/balances.html',mensaje)
    else:
        return redirect('contabilidad.views.balances')

def paginarLista(lista, pagina):
        contact_list = lista
        paginator = Paginator(contact_list, 5) # Show 25 contacts per page
        page = pagina
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return contacts

def contabilidad(request):
    if request.is_ajax():
        valor2= request.GET['num2']
        valor3= request.GET['num3']
        listaTransacciones = ''
        if len(valor3) == 0:
            listaTransacciones = Transaccion.objects.filter((Q(numero_cuenta__codigo__contains=valor2) | Q(numero_cuenta__nombre__icontains=valor2)))
        else:
            listaTransacciones = Transaccion.objects.filter(Q(fecha=valor3) &  (Q(numero_cuenta__codigo__contains=valor2) | Q(numero_cuenta__nombre__icontains=valor2)))
        listaTransacciones = paginarLista(listaTransacciones,request.GET.get('page'))
        data = serializers.serialize('json', listaTransacciones, use_natural_keys=True);
        return HttpResponse(data,content_type='aplication/json')
    else:
        contact_list = Transaccion.objects.all()
        paginator = Paginator(contact_list, 5) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        cuenta= PUC.objects.all()
        context2 = {"transacciones": contacts,"cuenta":cuenta}
        return render(request,'contabilidad/cuentasPorPagar.html', context2)


#def contabilidad(request):
#    istaTransacciones = Transaccion.objects.all()
#    pag = Paginador(request, istaTransacciones,10)
 #   context2 = {'lista': pag['modelo']}
   # return render(request,'contabilidad/cuentasPorPagar.html',context2)
   
def almacenarTransaccion(numeroCuenta,naturalezaT,conceptoT,valorT):
    cuenta= numeroCuenta
    nCuenta= cuenta.split(' ')
    naturaleza = naturalezaT
    valor= int(valorT)
    nf = nCuenta[0]
    concepto= conceptoT
    today = datetime.now() #fecha actual
    fecha = today.strftime("%Y-%m-%d")#Le damos un formato que admita la base de datos
    cuentaP= PUC.objects.get(pk=nf)#Buscamos esa cuenta para observar la naturaleza y asi establecer si el valor es positivo o negativo
    if cuentaP.naturaleza != naturaleza:#Si la naturaleza de la cuenta es diferente a la naturaleza de la transaccion el valor pasa a negativo
       valor= valor*(-1)
    transaccion = Transaccion(0,nf,concepto,valor,fecha,cuentaP.naturaleza)
    return transaccion
    
def validarCuentas(cuenta):
    nCuenta= cuenta.split(' ')
    nf = nCuenta[0]
    if len(nCuenta)>=3:
        try:
            cuentaP= PUC.objects.get(pk=nf)
            return True
        except:
            return False
    else:
        return False
        
def crearTransaccion(request):
    if request.method == 'POST':
        #Primero vemos si la cuenta 3 que es opcional tiene algun campo lleno
        #Si es asi tiene que estar todos para poder hacer toda la transaccion
        if validarCuentas(request.POST['cuenta']):
            #Primera Cuenta
            transaccion1= almacenarTransaccion(request.POST['cuenta'], request.POST['optionsRadios'], request.POST['concepto'], request.POST['valor'])
            try:
                    try:
                        transaccion1.save()#Guardamos primera cuenta
                        #Volvemos a la pagina inicial
                        listaTransacciones = Transaccion.objects.all()
                        listaTransacciones = paginarLista(listaTransacciones,request.GET.get('page'))
                        listaPUC= PUC.objects.all()
                        context = {'transacciones': listaTransacciones, 'cuenta': listaPUC}
                        return render(request,'contabilidad/cuentasPorPagar.html',context)
                    except IntegrityError, e:
                        context= errorCrearTransaccion('1',request.POST['cuenta'],request.POST['concepto'],request.POST['valor'])
                        return render(request,'contabilidad/cuentasPorPagar.html',context)
            except Error, e:
                #print e.message
                context= errorCrearTransaccion('2',request.POST['cuenta'],request.POST['concepto'],request.POST['valor'])
                return render(request,'contabilidad/cuentasPorPagar.html',context)
        else:
            #print e.message
            context= errorCrearTransaccion('3',request.POST['cuenta'],request.POST['concepto'],request.POST['valor'])
            return render(request,'contabilidad/cuentasPorPagar.html',context)
    else:
        return redirect('contabilidad.views.contabilidad')
    
# Reutilizacion de codigo. En caso de errores se hace lo mismo
def errorCrearTransaccion(request,cuenta,concepto,valor):
    listaTransacciones = Transaccion.objects.all()
    listaTransacciones = paginarLista(listaTransacciones,1)
    listaPUC= PUC.objects.all()
    msn='No se logro realizar la transaccion, Digite Valor valido '+request
    context = {'transacciones': listaTransacciones, 'cuenta': listaPUC,'mensaje': msn,'cuenta1':cuenta,'concepto':concepto,'valor':valor}
    return context
    
         