from django.urls import path
from django.contrib.auth.decorators import login_required
from aplicaciones.menu.views import *

urlpatterns = [
    path('empresas/', login_required(Empresas.as_view()), name='empresas'),
    path('empresa_inicial/', login_required(EmpresaInicial.as_view()),
         name='empresa_inicial'),
    path('<int:id>/', login_required(ObtenerMenu.as_view()), name='menu'),
]
