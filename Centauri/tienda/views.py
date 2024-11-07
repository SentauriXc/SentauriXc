from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Producto
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm
from .models import Producto
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Transaccion
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, redirect
from .models import Favorito, Producto

@login_required
def ver_favoritos(request):
    favoritos = Favorito.objects.filter(usuario=request.user).select_related('producto')
    return render(request, 'ver_favoritos.html', {'favoritos': favoritos})
@login_required
def toggle_favorito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    favorito, created = Favorito.objects.get_or_create(usuario=request.user, producto=producto)

    if not created:
        # Si ya existe, eliminar de favoritos
        favorito.delete()
    return redirect('lista_productos')  # Redirige a la lista de productos después de marcar/desmarcar
@login_required
def historial_transacciones(request):
    transacciones = Transaccion.objects.filter(comprador=request.user)
    return render(request, 'historial_transacciones.html', {'transacciones': transacciones})
@login_required
def comprar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        # Crear la transacción
        transaccion = Transaccion.objects.create(
            producto=producto,
            comprador=request.user,
            estado='completado'
        )
        return redirect('historial_transacciones')

    return render(request, 'confirmar_compra.html', {'producto': producto})

# Vista para añadir un nuevo producto
@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user  # Asigna el producto al usuario actual
            producto.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

# Vista para editar un producto existente
@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # Redirecciona después de editar
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})

# Vista para eliminar un producto existente
@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})

def perfil_usuario(request):
    return render(request, 'perfil_usuario.html')

# Vista para ver los detalles de un producto
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

# Vista para el registro de usuario
def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('lista_productos')  # Redirige a la lista de productos después del registro
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})
@login_required
def panel_usuario(request):
    productos = Producto.objects.filter(vendedor=request.user)
    transacciones = Transaccion.objects.filter(comprador=request.user)
    return render(request, 'panel_usuario.html', {
        'productos': productos,
        'transacciones': transacciones
    })
def lista_productos(request):
    query = request.GET.get('q', '')
    min_precio = request.GET.get('min_precio')
    max_precio = request.GET.get('max_precio')
    estado = request.GET.get('estado')

    productos = Producto.objects.all()

    if query:
        productos = productos.filter(nombre__icontains=query)

    if min_precio:
        productos = productos.filter(precio__gte=min_precio)

    if max_precio:
        productos = productos.filter(precio__lte=max_precio)

    if estado:
        productos = productos.filter(estado=estado)

    # Marcar cada producto como favorito o no para el usuario actual
    favoritos = Favorito.objects.filter(usuario=request.user).values_list('producto_id', flat=True)
    for producto in productos:
        producto.es_favorito = producto.id in favoritos

    return render(request, 'lista_productos.html', {
        'productos': productos,
        'query': query,
        'min_precio': min_precio,
        'max_precio': max_precio,
        'estado': estado
    })


