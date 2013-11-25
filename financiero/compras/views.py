# Create your views here.
import json
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from compras.models import Proveedor, Producto_Proveedor, Compra, Compra_Producto
from django.db import IntegrityError
from django.core.paginator import Paginator
from inventario.models import Producto
from django.core import serializers
from django.db.models import Q, F, Sum, Count
from django.utils import timezone
from django.db import connection
from django.core.urlresolvers import reverse

#Paginacion
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

def buscarProductos(request):
	if request.method == 'GET':
		if request.is_ajax():
			codigo = request.GET['proveedor']
			lista = Producto.objects.filter(producto_proveedor__proveedor=codigo)
			data = serializers.serialize('json', lista)
			return HttpResponse(data, mimetype='aplication/json')
		else:
			return redirect('compras.views.indexCompras')
	else:
		return redirect('compras.views.indexCompras')

def buscarPrecioProductoProveedor(request):
	if request.method == 'GET':
		if request.is_ajax():
			producto = request.GET['producto']
			proveedor = request.GET['proveedor']
			lista = Producto_Proveedor.objects.get(Q(producto=producto) & Q(proveedor=proveedor))
			data = serializers.serialize('json', [lista])
			return HttpResponse(data, mimetype='aplication/json')
		else:
			return redirect('compras.views.indexCompras')
	else:
		return redirect('compras.views.indexCompras')

#Vistas de Compras
def indexCompras(request):
	try:
		pag=request.GET['pag']
	except:
		pag="*1"
	listaCompras = Compra.objects.all()
	if request.is_ajax():
		info = paginacionAjax(listaCompras, pag)
		data = serializers.serialize('json', info, use_natural_keys=True);
		return HttpResponse(data,mimetype='aplication/json')
	else:
		#Se quitan los proveedores de estado inactivo
		proveedores = Proveedor.objects.exclude(estado=False)
		info = paginacionCompras(listaCompras, pag, proveedores)
		return render(request, 'compras/index.html', info)

def agregarCompra(request):
	if request.method == 'POST':
		#Datos para la creacion de la compra
		proveedor = request.POST['proveedor']
		try:
			proveedorDatos = Proveedor.objects.get(pk=proveedor)
			descripcion = request.POST['descripcion']
			fecha = timezone.now()
			compra = Compra(descripcion=descripcion, fecha=fecha, proveedor=proveedorDatos)
			compra.save()
			try:
				#Informacion para el renderizado de la pagina respuesta
				proveedores = Proveedor.objects.exclude(estado=False)
				listaCompras = Compra.objects.all()
				#Datos para la creacion de la relacion producto compra
				cantidadProductos = int(request.POST['cantidadproductos'])
				for a in range(0, cantidadProductos + 1):
					auxProducto = 'productos_' + `a`
					productoPedido = request.POST[auxProducto]
					if (productoPedido != "-1"):
						try:
							infoProducto = Producto.objects.get(pk=productoPedido)
							auxPrecio = 'precio_' + `a`
							productoPrecio = request.POST[auxPrecio]
							auxCantidad = 'cantidad_' + `a`
							productoCantidad = request.POST[auxCantidad]
							#Se crea el objecto de la relacion entre compra y producto
							infoProducto.cantidad = infoProducto.cantidad + int(productoCantidad)
							infoProducto.save()
							relacion = Compra_Producto(cantidad = productoCantidad, precio=productoPrecio, compra=compra, producto=infoProducto)
							relacion.save()
						except Producto.DoesNotExist:
							info = paginacionCompras(listaCompras, "*1", proveedores, "Ocurrio un problema al guardar la compra, por favor verifique la informacion del producto e intentelo mas tarde", 2)
							return render(request, 'compras/index.html', info)
				info = paginacionCompras(listaCompras, "*1", proveedores, "La compra se guardo satisfactoriamente", 1)
				return render(request, 'compras/index.html', info)
				#return redirect('compras.views.indexCompras')
			except Proveedor.DoesNotExist:
				info = paginacionCompras(listaCompras, "*1", proveedores, "Ocurrio un problema al guardar la compra, por favor verifique la informacion del proveedor e intentelo mas tarde", 2)
				return render(request, 'compras/index.html', info)
		except Exception as e:
			return redirect('compras.views.indexCompras')
	else:
		print "Aqui 3"
		return redirect('compras.views.indexCompras')

def listadoCompras(request):
	if request.is_ajax():
		codigoCompra = request.GET['codigoCompra']
		#Se obtiene la info de la compra
		infoCompra = Compra.objects.get(pk=codigoCompra)
		#Se obtiene la relacion de la compra y el producto
		compraProducto = Compra_Producto.objects.filter(compra=infoCompra)
		data = serializers.serialize('json', compraProducto, use_natural_keys = True);
		return HttpResponse(data, mimetype="aplication/json")
	else:
		return redirect('compras.views.indexCompras')

def buscarCompra(request):
	if request.is_ajax():
		array = True
		listaCompras = Compra.objects.all()
		descripcion = request.GET['busquedaDescripcion']
		listaCompras = listaCompras.filter(descripcion__icontains=descripcion)
		proveedor = request.GET['busquedaProveedor']
		listaCompras = listaCompras.filter(proveedor__nombre__icontains=proveedor).order_by('codigo')
		fecha = request.GET['busquedaFecha']
		if len(fecha) > 0:
			listaCompras = listaCompras.filter(fecha=fecha)
		codigo = request.GET['busquedaCodigo']
		if len(codigo) > 0:
			try:
				finCodigo = int(codigo)
			except:
				finCodigo = 0
			if finCodigo > 0:
				try:
					listaCompras = listaCompras.get(pk=finCodigo)
					array = False
				except Compra.DoesNotExist:
					listaCompras = []
			else:
				listaCompras = []
		if array:
			try:
				pag=request.GET['pag']
			except:
				pag="*1"
			info = paginacionAjax(listaCompras, pag)
			data = serializers.serialize('json', info, use_natural_keys=True);
			return HttpResponse(data,mimetype='aplication/json')
		else:
			data=serializers.serialize('json',[listaCompras], use_natural_keys=True);
			return HttpResponse(data,mimetype='aplication/json')
	else:
		return redirect('compras.views.indexCompras')

def paginacionCompras(listaDatos, pag, listaProveedores=[], mensaje="", tipoMensaje=0):
	num = len(listaDatos)
	datosPaginacion = Paginator(listaDatos, 10);
	cont = datosPaginacion.num_pages;
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
	return {'listaCompras': info, 'pag':pag, 'cont':cont, 'mensaje':mensaje, 'tipoMensaje':tipoMensaje, 'proveedores':listaProveedores}

#Vistas de proveedor
def indexProveedor(request, mensaje="", tipoMensaje=0):
	try:
		pag=request.GET['pag']
	except:
		pag="*1"
	listaProveedores = Proveedor.objects.all()
	print (request.session.get('error_message','')), "Aqui vamos Bn"
	if request.is_ajax():
		info = paginacionAjax(listaProveedores, pag)
		data = serializers.serialize('json',info)
		return HttpResponse(data,mimetype='aplication/json')
	else:
		info = paginacionProv(listaProveedores, pag, mensaje, tipoMensaje)
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
			info = paginacionProv(listaProveedores, pag, "El Proveedor no se ha podido agregar, revise el codigo", 2)
		except Proveedor.DoesNotExist:
			proveedor = Proveedor(codigo,nombre,direccion,telefono,estado)
			try:
				#proveedor.save()
				info = paginacionProv(listaProveedores, pag, "El proveedor se ha agregado Correctamente", 1)
			except IntegrityError:
				info = paginacionProv(listaProveedores, pag, "El Proveedor no se ha podido agregar, revise el telefono", 3)
		return render(request, 'proveedor/index.html', info)
		#return redirect(reverse('compras.views.indexProveedor', mensaje=mensaje))
		#return HttpResponseRedirect(reverse('compras.views.indexProveedor',args=(mensaje,)))
		#return redirect('compras.views.indexProveedor')
	else:
		return redirect('compras.views.indexProveedor')

def editarProveedor(request):
	if request.method == 'POST':
		codigo = request.POST['nuevoCodigo']
		nombre = request.POST['nuevoNombre']
		direccion = request.POST['nuevaDireccion']
		telefono = request.POST['nuevoTelefono']
		estado = request.POST['nuevoEstado']
		pag="*1"
		try:
			proveedor = Proveedor.objects.get(pk=codigo)
			try:
				if(len(nombre) > 0):
					proveedor.nombre = nombre
				if(len(direccion) > 0):
					proveedor.direccion = direccion
				if(len(telefono) > 0):
					proveedor.telefono = telefono
				if request.POST['nuevoEstado'] == "1":
					proveedor.estado = True
				else:
					proveedor.estado = False
				proveedor.save()
				listaProveedores = Proveedor.objects.all()
				mensaje = 1
				info = paginacionProv(listaProveedores, pag, "El proveedor se ha modificado correctamente", 1)
			except IntegrityError:
				listaProveedores = Proveedor.objects.all()
				info = paginacionProv(listaProveedores, pag, "El Proveedor no se ha podido modificar, revise el telefono", 3)
		except Proveedor.DoesNotExist:
			listaProveedores = Proveedor.objects.all()
			info = paginacionProv(listaProveedores, pag, "El Proveedor no se ha podido modificar, revise el codigo", 2)
		return render(request, 'proveedor/index.html', info)
		#return redirect('compras.views.indexProveedor', "mensaje", 1)
	else:
		return redirect('compras.views.indexProveedor')

#1-Agregado Correcto
#2-Fallo
def paginacionProv(listaDatos, pag, mensaje="", tipoMensaje=0):
	num = len(listaDatos)
	datosPaginacion = Paginator(listaDatos, 10);
	cont = datosPaginacion.num_pages;
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