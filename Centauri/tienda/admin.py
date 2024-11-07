from django.contrib import admin
from .models import Producto, Transaccion

admin.site.register(Producto)
admin.site.register(Transaccion)