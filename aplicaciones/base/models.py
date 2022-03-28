from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.urls import re_path, path
from aplicaciones.base.base_crud.views_crud import BaseCrear, BaseListar, BaseActualizar, BaseEliminarLogico, BaseListarValores
from aplicaciones.base.base_reportes import ObtenerReporteExcel
from aplicaciones.base.utils import *


class ModeloBase(models.Model):
    """ MODELO BASE PARA CREACIÓN DE CRUDS AUTOMÁTICOS.

    Este modelo es la base para la creación de todos los demás modelos los cuales se deseen crear sus CRUDS básicos,
    crea todas las URLS necesarias para dichas funciones, ofrece las funcionalidades básicas, pudiendo sobreescribir
    dichas funcionalidades heredando de las Vistas Genéricas correspondientes.

    Funciona llamando al método -- construir_URLS_genericas_de_CRUD -- el cual retorna -- urlpatterns -- que contienen
    las rutas generadas automaticamente para cada modelo, les asigna tanto un nombre a cada URL como una ruta como tal.

    Los métodos que tienen en su nombre -- alias -- son los nombre asociados a las URLS.

    Un ejemplo de cómo realizar esto es el siguiente:

        Supongamos que tenemos un modelo llamado Persona, el cuál gestionaremos a través de nuestro CRUD automático, para
        ello deberemos hacer que herede de ModeloBase:

        class Persona(ModeloBase):
            -- Aquí definimos sus campos, recordemos que ya cuenta con una clave primaria llamada id definida en el modelo
               base.

            -- Podemos definir funciones que deseemos.


        Esto se haría en el archivo models.py, lo siguiente sería dirigirnos al archivo urls.py, donde haríamos lo siguiente:

            from django.urls import path
            from .models import Persona

            urlpatterns = [

            ]

            -- Aquí instanciamos nuestro modelo de la siguiente manera:

                persona = Persona()

            -- Luego llamamos al metodo que construye nuestras rutas y por lo tanto nuestro CRUD automático:

                urlpatterns += persona.construir_URLS_genericas_de_CRUD('aplicación','Persona')

            -- Hay que saber que los parámetros enviados a la función construir_URLS_genericas_de_CRUD son los siguientes:

                    _app_name   : Cadena de texto con el nombre de la aplicación donde se encuentra el modelo a utilizar.
                    _model_name : Cadena de texto con el nombre del modelo a buscar en el proyecto.



    """
    id = models.AutoField(primary_key=True)
    estado = models.BooleanField('Estado', default=True)
    fecha_creacion = models.DateField(
        'Fecha de Creación', auto_now_add=True, auto_now=False)
    fecha_modificacion = models.DateField(
        'Fecha de Modoficación', auto_now=True, auto_now_add=False)
    fecha_eliminacion = models.DateField(
        'Fecha de Eliminación', auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse(self.get_absolute_url_alias(), kwargs={'object_id': self.id})

    def get_crear_url(self):
        return reverse(self.get_crear_url_alias())

    def get_listar_url(self):
        return "/%s/%s/" % (self._meta.app_label, self._meta.module_name)

    def get_eliminar_url(self):
        return reverse(self.get_eliminar_url_alias(), kwargs={'object_id': self.id})

    def get_actualizar_url(self):
        return reverse(self.get_actualizar_url_alias(), kwargs={'object_id': self.id})

    def get_values_regexp(self):
        return "{0}/valores/".format(self._meta.object_name.lower())

    def get_crear_url_regexp(self):
        return '{0}/crear/'.format(self._meta.object_name.lower())

    def get_listar_url_regexp(self):
        return "{0}/".format(self._meta.object_name.lower())

    def get_eliminar_url_regexp(self):
        return "{0}/<int:pk>/eliminar/".format(self._meta.object_name.lower())

    def get_actualizar_url_regexp(self):
        return "{0}/<int:pk>/actualizar/".format(self._meta.object_name.lower())

    def get_reporte_excel_regexp(self):
        return "{0}/reportes/{1}/".format(self._meta.object_name.lower(), self._meta.object_name.lower())

    def get_absolute_url_alias(self):
        return "{0}_{1}_absolute".format(self._meta.app_label, self._meta.object_name.lower())

    def get_crear_url_alias(self):
        return '{0}_{1}_crear'.format(self._meta.app_label, self._meta.object_name.lower())

    def get_listar_url_alias(self):
        return "{0}_{1}_listar".format(self._meta.app_label, self._meta.object_name.lower())

    def get_eliminar_url_alias(self):
        return "{0}_{1}_eliminar".format(self._meta.app_label, self._meta.object_name.lower())

    def get_actualizar_url_alias(self):
        return "{0}_{1}_actualizar".format(self._meta.app_label, self._meta.object_name.lower())

    def get_reporte_excel_alias(self):
        return "{0}_{1}_reporte_excel".format(self._meta.app_label, self._meta.object_name.lower())

    def construir_URLS_genericas_de_CRUD(self, _app_name, _model_name, _form):
        # Se obtiene el modelo en cuestión a través de la cadena de texto que menciona a la aplicación donde está dicho modelo,
        # y la cadena de texto con el nombre del modelo a buscar en el proyecto.
        _modelo = obtener_modelo(_app_name, _model_name)
        urlpatterns = [
            path(self.get_listar_url_regexp(), login_required(BaseListar.as_view()), {
                 'modelos': _modelo}, name=self.get_listar_url_alias()),
            path(self.get_values_regexp(), login_required(BaseListarValores.as_view()), {
                 'modelos': _modelo}, name=self.get_absolute_url_alias()),
            path(self.get_crear_url_regexp(), login_required(BaseCrear.as_view()), {
                 'model': _modelo, 'form': _form}, name=self.get_crear_url_alias()),
            path(self.get_actualizar_url_regexp(), login_required(BaseActualizar.as_view()), {
                 'modelos': _modelo, 'form': _form}, name=self.get_actualizar_url_alias()),
            path(self.get_eliminar_url_regexp(), login_required(BaseEliminarLogico.as_view()), {
                 'modelos': _modelo}, name=self.get_eliminar_url_alias()),
            path(self.get_reporte_excel_regexp(), login_required(ObtenerReporteExcel.as_view()), {
                 '_app_name': _app_name, '_model_name': _model_name}, name=self.get_reporte_excel_alias()),
        ]
        return urlpatterns
