from django.db import models
from django.contrib.auth.models import User

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'producto')  # Evita duplicados de usuario-producto

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"

# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[('nuevo', 'Nuevo'), ('usado', 'Usado')])
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Transaccion(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    comprador = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completado', 'Completado')])

    def __str__(self):
        return f"{self.producto.nombre} - {self.comprador.username} - {self.estado}"
