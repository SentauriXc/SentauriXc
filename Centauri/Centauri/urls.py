from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tienda/', include('tienda.urls')),  # Asegúrate de que esta línea esté apuntando a la app "tienda"
]
