# Create your views here.
from inventory.models import Bodega, Producto
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from datetime import *

def create_product(request):
	if request.method == 'POST':
		nombre = request.POST['nombre'];
		descripcion = request.POST['descripcion'];
		medida = request.POST['medida'];
		minimo = request.POST['minimo'];
		cantidad = request.POST['cantidad'];
		bodega = request.POST['bodega'];
		time=datetime.today()
		format=time.strftime('%Y-%m-%d %H:%M:%S')
		bodega = Bodega.objects.all();
		Producto.objects.create(nombre=nombre, descripcion=descripcion, medida=medida, inventario_minimo=minimo, fecha_ingreso=format, bodega_id=bodega);
		return HttpResponseRedirect('/products')
	else:
		product = Producto.objects.all();
		return render_to_response('create_product.html', context_instance=RequestContext(request));

def create_cellar(request):
	if request.method == 'POST':
		nombre = request.POST['nombre'];
		direccion = request.POST['direccion'];
		Bodega.objects.create(nombre=nombre, direccion=direccion);
		return HttpResponseRedirect('/cellars')
	else:
		bodega = Bodega.objects.all();
		return render_to_response('create_cellar.html', context_instance=RequestContext(request));

def table_cellar(request):
	cellar = Bodega.objects.all();
	return render_to_response('cellars.html',{'cellar':cellar})


