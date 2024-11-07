from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('producto/agregar/', views.agregar_producto, name='agregar_producto'),
    path('producto/<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),
    path('producto/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('producto/<int:producto_id>/comprar/', views.comprar_producto, name='comprar_producto'),
    path('transacciones/', views.historial_transacciones, name='historial_transacciones'),
    path('panel/', views.panel_usuario, name='panel_usuario'),
    path('producto/<int:producto_id>/favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('favoritos/', views.ver_favoritos, name='ver_favoritos'),
]
