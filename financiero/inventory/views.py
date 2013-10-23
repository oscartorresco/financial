# Create your views here.
from inventory.models import Bodega, Producto
from inventory.forms import ProductForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import *

def create_product(request):
	if request.method == 'POST':
		nombre = request.POST['nombre'];
		descripcion = request.POST['descripcion'];
		medida = request.POST['medida'];
		minimo = request.POST['minimo'];
		cantidad = request.POST['cantidad'];
		bodega = request.POST['bodega'];
		image = request.POST['imagen'];
		time = datetime.today()
		format = time.strftime('%Y-%m-%d')
		Producto.objects.create(nombre=nombre, descripcion=descripcion, medida=medida, inventario_minimo=minimo, cantidad=cantidad, fecha_ingreso=format, bodega_id=bodega);
		photo = impleUploadedFile('imagencliente.jpg', buf.getvalue(), "image/jpeg")
		return HttpResponseRedirect('/cellars')
	else:
		bodegas = Bodega.objects.all()
		return render_to_response('create_product.html',{'bodegas': bodegas}, context_instance=RequestContext(request))

def create_cellar(request):
	if request.method == 'POST':
		nombre = request.POST['nombre'];
		direccion = request.POST['direccion'];
		Bodega.objects.create(nombre=nombre, direccion=direccion);
		return HttpResponseRedirect('/cellars')
	else:
		bodegas = Bodega.objects.all()
		return render_to_response('create_cellar.html', context_instance=RequestContext(request))

def table_cellar(request):
	bodegas = Bodega.objects.all()
	return render_to_response('cellars.html',{'bodegas': bodegas}, context_instance=RequestContext(request))

def example(request):
    if request.method=='POST':
        formulario = ProductForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/cellars')
    else:
        formulario = ProductForm()
    	return render_to_response('example.html',{'formulario':formulario}, context_instance=RequestContext(request))

