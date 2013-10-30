# Create your views here.
from inventario.models import Bodega, Producto
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from datetime import *

def crear_producto(request):
	if request.method == 'POST':
		nombre = request.POST['nombre']
		descripcion = request.POST['descripcion']
		medida = request.POST['medida']
		minimo = request.POST['minimo']
		cantidad = request.POST['cantidad']
		bodega = request.POST['bodega']
		image = request.FILES.get("imagen")
		estado = True
		time = datetime.today()
		format = time.strftime('%Y-%m-%d')	
		producto = Producto.objects.create(nombre=nombre, descripcion=descripcion, medida=medida, inventario_minimo=minimo, cantidad=cantidad, imagen=image, fecha_ingreso=format, bodega_id=bodega, estado=estado);
		producto.save()
		return redirect('inventario.views.tabla_productos')
	else:
		bodegas = Bodega.objects.all()
		return render_to_response('index.html',{'bodegas': bodegas}, context_instance=RequestContext(request))

def crear_bodega(request):
	if request.method == 'POST':
		nombre = request.POST['nombre']
		direccion = request.POST['direccion']
		Bodega.objects.create(nombre=nombre, direccion=direccion)
		return HttpResponseRedirect('/cellars')
	else:
		bodegas = Bodega.objects.all()
		return render_to_response('create_cellar.html', context_instance=RequestContext(request))

def tabla_bodegas(request):
	bodegas = Bodega.objects.all()
	return render_to_response('cellars.html',{'bodegas': bodegas}, context_instance=RequestContext(request))

def tabla_productos(request):
	productos = Producto.objects.all()
	return render_to_response('index.html',{'productos': productos}, context_instance=RequestContext(request))
