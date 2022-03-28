from django.urls import path
from django.contrib.auth.decorators import login_required
from aplicaciones.usuarios.views import *

urlpatterns = [
    path('usuarios/usuario/',login_required(InicioUsuario.as_view()), name = 'inicio_usuario'),
    path('eliminar_usuario/<int:id>/',login_required(EliminarUsuario.as_view()), name = 'eliminar_usuario'),
    path('actualizar_usuario/<int:id>/',login_required(ActualizarUsuario.as_view()), name = 'actualizar_usuario'),
    path('reporte_usuarios_excel/',login_required(ReporteUsuarioExcel.as_view()), name = 'reporte_usuarios_excel'),
]
