from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Producto, Favorito, Transaccion

class TiendaTests(TestCase):

    def setUp(self):
        # Crear usuarios de prueba
        self.usuario = User.objects.create_user(username='testuser', password='testpass')
        self.usuario_vendedor = User.objects.create_user(username='vendedor', password='vendedorpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

        # Crear un producto de prueba con el usuario como vendedor
        self.producto = Producto.objects.create(
            nombre='Camisa',
            descripcion='Camisa de algodón',
            precio=50,
            estado='nuevo',
            vendedor=self.usuario_vendedor
        )

    def test_registro_usuario(self):
        response = self.client.post(reverse('registro'), {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_inicio_sesion_usuario(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)

    def test_agregar_producto(self):
        self.client.login(username='vendedor', password='vendedorpass')
        response = self.client.post(reverse('agregar_producto'), {
            'nombre': 'Sombrero',
            'descripcion': 'Sombrero de lana',
            'precio': 30,
            'estado': 'nuevo',
            'vendedor': self.usuario_vendedor.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Producto.objects.filter(nombre='Sombrero').exists())

    def test_editar_producto(self):
        self.client.login(username='vendedor', password='vendedorpass')
        response = self.client.post(reverse('editar_producto', args=[self.producto.id]), {
            'nombre': 'Camisa Editada',
            'descripcion': 'Camisa de algodón editada',
            'precio': 55,
            'estado': 'usado'
        })
        self.assertEqual(response.status_code, 302)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Camisa Editada')

    def test_eliminar_producto(self):
        self.client.login(username='vendedor', password='vendedorpass')
        response = self.client.post(reverse('eliminar_producto', args=[self.producto.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Producto.objects.filter(id=self.producto.id).exists())

    def test_busqueda_producto(self):
        response = self.client.get(reverse('lista_productos') + '?q=Camisa')
        self.assertContains(response, 'Camisa')

    def test_filtro_precio_y_estado(self):
        response = self.client.get(reverse('lista_productos') + '?min_precio=40&max_precio=60&estado=nuevo')
        self.assertContains(response, 'Camisa')

    def test_marcar_favorito(self):
        response = self.client.get(reverse('toggle_favorito', args=[self.producto.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Favorito.objects.filter(usuario=self.usuario, producto=self.producto).exists())

    def test_desmarcar_favorito(self):
        Favorito.objects.create(usuario=self.usuario, producto=self.producto)
        response = self.client.get(reverse('toggle_favorito', args=[self.producto.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Favorito.objects.filter(usuario=self.usuario, producto=self.producto).exists())

    def test_compra_exitosa(self):
        # Prueba de compra exitosa
        response = self.client.post(reverse('comprar_producto', args=[self.producto.id]), follow=True)
        transaccion = Transaccion.objects.filter(comprador=self.usuario, producto=self.producto).first()
        self.assertIsNotNone(transaccion)
        self.assertEqual(transaccion.estado, 'completado')  # Cambiado a 'completada'
        self.assertEqual(response.status_code, 200)

    def test_compra_producto_inexistente(self):
        # Prueba de compra de producto inexistente
        response = self.client.post(reverse('comprar_producto', args=[999]), follow=True)
        self.assertEqual(response.status_code, 404)
