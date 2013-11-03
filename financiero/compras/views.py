# Create your views here.
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from compras.models import Proveedor, Producto_Proveedor, Compra
from django.db import IntegrityError
from django.core.paginator import Paginator
from inventario.models import Producto
from django.core import serializers

#Vistas de Compras
def indexCompras(request):
	listaCompras = Compra.objects.all()
	paginat= Paginator(lista,10);
	context = {'listaCompras':listaCompras}
	return render(request, 'compras/index.html', context)

def agregarCompra(request):
	return HttpResponse("Shedman")

#Vistas de proveedor
def indexProveedor(request):
	try:
		pag=request.GET['pag']
	except:
		pag="*1"
	listaProveedores = Proveedor.objects.all()
	if request.is_ajax():
		info = paginacionAjax(listaProveedores, pag)
		data = serializers.serialize('json',info);
		return HttpResponse(data,mimetype='aplication/json')
	else:
		info = paginacion(listaProveedores, pag)
		return render(request, 'proveedor/index.html', info)

def agregarProveedor(request):
	if request.method == 'POST':
		codigo = request.POST['codigo']
		nombre = request.POST['nombre']
		direccion = request.POST['direccion']
		telefono = request.POST['telefono']
		estado = True
		listaProveedores = Proveedor.objects.all()
		pag="*1"
		try:
			aux = Proveedor.objects.get(pk=codigo)
			info = paginacion(listaProveedores, pag, "El Proveedor no se ha podido agregar, revise el codigo", 2)
		except Proveedor.DoesNotExist:
			proveedor = Proveedor(codigo,nombre,direccion,telefono,estado)
			try:
				proveedor.save()
				info = paginacion(listaProveedores, pag, "El proveedor se ha agregado Correctamente", 1)
			except IntegrityError:
				info = paginacion(listaProveedores, pag, "El Proveedor no se ha podido agregar, revise el telefono", 3)
		return render(request, 'proveedor/index.html', info)
	else:
		return render(request, 'proveedor/agregar.html')

def paginacionAjax(listaDatos, pag):
	num = len(listaDatos)
	datosPaginacion = Paginator(listaDatos, 10);
	cont=datosPaginacion.num_pages;
	if pag[:1] == '*':
		pag = pag.strip('*')
		pag = int(pag) - 1
		if(int(pag) == 0):
			pag = 1
	else:
		if pag[:1] == '^':
			pag = pag.strip('^')
			pag = int(pag) + 1
			if int(pag) > cont:
				pag = cont
	if int(pag) > 0 and int(pag) <= cont:
		info = datosPaginacion.page(int(pag))
	else:
		info = datosPaginacion.page(1)
	if(num == 0):
		cont = 0
	return info

#1-Agregado Correcto
#2-Fallo
def paginacion(listaDatos, pag, mensaje="", tipoMensaje=0):
	num = len(listaDatos)
	datosPaginacion = Paginator(listaDatos, 10);
	cont=datosPaginacion.num_pages;
	if pag[:1] == '*':
		pag = pag.strip('*')
		pag = int(pag) - 1
		if(int(pag) == 0):
			pag = 1
	else:
		if pag[:1] == '^':
			pag = pag.strip('^')
			pag = int(pag) + 1
			if int(pag) > cont:
				pag = cont
	if int(pag) > 0 and int(pag) <= cont:
		info = datosPaginacion.page(int(pag))
	else:
		info = datosPaginacion.page(1)
	if(num == 0):
		cont = 0
	return {'listaProveedores': info, 'pag':pag, 'cont':cont, 'mensaje':mensaje, 'tipoMensaje':tipoMensaje}

def buscarProveedor(request):
	if request.is_ajax():
		array = True
		listaProveedores = Proveedor.objects.all()
		nombre = request.GET['busquedaNombre']
		listaProveedores = listaProveedores.filter(nombre__icontains=nombre)
		direccion = request.GET['busquedaDireccion']
		listaProveedores = listaProveedores.filter(direccion__icontains=direccion)
		codigo = request.GET['busquedaCodigo']
		if len(codigo) > 0:
			try:
				listaProveedores = listaProveedores.get(pk=codigo)
				array = False
			except Proveedor.DoesNotExist:
				listaProveedores = []
		telefono = request.GET['busquedaTelefono']
		if len(telefono) > 0:
			try:
				listaProveedores = listaProveedores.get(telefono=telefono)
				array = False
			except Proveedor.DoesNotExist:
				listaProveedores = []
		if array:
			try:
				pag=request.GET['pag']
			except:
				pag="*1"
			info = paginacionAjax(listaProveedores, pag)
			data = serializers.serialize('json', info);
			return HttpResponse(data, mimetype='aplication/json')
		else:
			data=serializers.serialize('json',[listaProveedores]);
			return HttpResponse(data,mimetype='aplication/json')
	else:
		return redirect('compras.views.indexProveedor')

def editarProveedor(request, codigo_proveedor):
	if request.method == 'POST':
		prov = get_object_or_404(Proveedor, pk=codigo_proveedor)
		if len(request.POST['nuevaDireccion']) > 0:
			prov.direccion = request.POST['nuevaDireccion']
		if request.POST['estado'] == "true":
			prov.estado = True
		else:
			prov.estado = False
		prov.save()
		return redirect('compras.views.indexProveedor')
	else:
		return render(request, 'proveedor/index.html')

def listaProductosProveedor(request, codigo_proveedor):
	listaAuxiliar = Producto_Proveedor.objects.filter(proveedor = codigo_proveedor)
	#listaProductos = get_list_or_404(Producto, pk=listaAuxiliar__producto)
	proveedor = get_object_or_404(Proveedor, pk=codigo_proveedor)
	return render(request, 'proveedor/detalle.html', {'listaAuxiliar':listaAuxiliar,'proveedor':proveedor})

def agregarProductoProveedor(request, codigo_proveedor):
	if request.method == 'POST':
		HttpResponse("Formulario Enviado")
	else:
		listaProductos = Producto.objects.all()
		return render(request, 'proveedor/agregar_Producto.html', {'listaProductos':listaProductos})