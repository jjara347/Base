from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import Inicio

urlpatterns = [
    path('',login_required(Inicio.as_view()), name = 'inicio'),
]
