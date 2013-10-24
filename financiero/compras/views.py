# Create your views here.
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from compras.models import Proveedor, Producto_Proveedor, Compra
from inventory.models import Producto

#Vistas de Compras
def indexCompras(request):
	listaCompras = Compra.objects.all()
	context = {'listaCompras':listaCompras}
	return render(request, 'compras/index.html', context)

def agregarCompra(request):
	return HttpResponse("Shedman")

#Vistas de proveedor
def indexProveedor(request):
    listaProveedores = Proveedor.objects.all()
    context = {'listaProveedores': listaProveedores}
    return render(request, 'proveedor/index.html', context)

def agregarProveedor(request):
	if request.method == 'POST':
		codigo = request.POST['codigo']
		nombre = request.POST['nombre']
		direccion = request.POST['direccion']
		telefono = request.POST['telefono']
		estado = True
		proveedor = Proveedor(codigo,nombre,direccion,telefono,estado)
		proveedor.save()
		return redirect('compras.views.indexProveedor')
	else:
		return render(request, 'proveedor/agregar.html')

def editarProveedor(request, codigo_proveedor):
	if request.method == 'POST':
		prov = get_object_or_404(Proveedor, pk=codigo_proveedor)
		prov.nombre = request.POST['nombre']
		prov.direccion = request.POST['direccion']
		prov.telefono = request.POST['telefono']
		#Preguntar si esto es posible de otra manera
		if request.POST['estado'] == "true":
			prov.estado = True
		else:
			prov.estado = False
		prov.save()
		return redirect('compras.views.indexProveedor')
	else:
		proveedor = get_object_or_404(Proveedor, pk=codigo_proveedor)
		return render(request, 'proveedor/editar.html', {'proveedor':proveedor})

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