import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import CreateView, ListView, View, DeleteView, UpdateView, DetailView, TemplateView
from django.core.serializers import serialize
from django.forms.models import modelform_factory, model_to_dict
from aplicaciones.base.forms import FormularioLogin
from aplicaciones.base.utils import convertir_booleanos


class BaseCrear(CreateView):
    """ REGISTRAR UNA NUEVA INSTANCIA DE UN MODELO.

    Su función es registrar en la base de datos una nueva instancia de un modelo en cuestión,
    dicho modelo es pasado por parámetro a través del método post redefinido en la clase.

    Variables:
    -- model                        : modelo a utilizarse.
    -- template_403                 : template que renderiza el error 403 de acción prohibida.

    Metodos:
    -- post                         : método a ejecutarse que registrará la nueva instancia del modelo.
                                      El método asigna el modelo enviado por parámetro al modelo de la clase
                                      para luego verificar si existen campos de tipo Booleanos enviados desde el
                                      frontend, tomando como diccionario el contenido y devolviendolo validado,
                                      luego de ello se registra una nueva instancia de un Form perteneciente al modelo
                                      que se está trabajando, esto a través del método --modelform_factory -- definiendo
                                      que tome todos los parámetros de este modelo, luego se le asigna la información
                                      que ya ha sido validada en el paso anterior para que Django asigne automaticamente
                                      cada campo a su correspondiente atributo para posteriormente validar este Form y
                                      proceder a guardar en la base de datos la información, retornando una instancia de
                                      JsonResponse con un mensaje de éxito y el código HTTP 201 CREATED.

                                      En caso la información asignada al Form no sea válida, se devuelve una instancia de
                                      JsonResponse con el mensaje de error y los errores que el Form ha detectado y generado
                                      junto con el códgo HTTP 400 BAD REQUEST.

                                      Todo esto se lleva a cabo si la petición ha sido enviada a través de una solicitud AJAX,
                                      en caso no sea así se mostrará un template de error 403 FORBIDDEN.


    """
    model = None
    template_403 = '403.html'

    def post(self, request, model, form, *args, **kwargs):
        if request.is_ajax():
            self.model = model
            request.POST._mutable = True
            request.POST['estado'] = True
            data = request.POST
            data = convertir_booleanos(data)
            formulario = modelform_factory(model=self.model,form=form)
            formulario = formulario(data)
            if formulario.is_valid():
                formulario.save()
                mensaje = "{0} registrado correctamente!".format(
                    self.model.__name__)
                error = 'Ninguno'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = "{0} no se ha podido registrar!".format(
                    self.model.__name__)
                error = formulario.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return render(request, self.template_403)


class BaseListar(ListView):
    """ LISTAR INFORMACIÓN PERTENECIENTE A UN MODELO SERIALIZANDO AUTOMATICAMENTE.

    Su función es mostrar un listado de los registros pertenecientes al modelo en cuestión que se desea utilizar.

    Variables:
    -- model                        : modelo a utilizarse.
    -- queryset                     : consulta a realizarse.
    -- data_usuario                 : datos de consulta serializados en formato JSON.
    -- template_403                 : template que renderiza el error 403 de acción prohibida.

    Metodos:
    -- get                          : método a ejecutarse que retornará todos los datos pertenecientes al modelo alojado en la variable
                                      -- model -- obtenidos a través de la variable -- queryset -- en formato JSON.

                                      Todo esto se lleva a cabo si la petición ha sido enviada a través de una solicitud AJAX,
                                      en caso no sea así se mostrará un template de error 403 FORBIDDEN.


    """
    model = None
    data = None
    template_403 = '403.html'

    def get_queryset(self):
        return self.model.objects.filter(estado=True)

    def get(self, request, modelos, *args, **kwargs):
        if request.is_ajax():
            self.model = modelos
            self.data = serialize('json', self.get_queryset(
            ), use_natural_foreign_keys=True)
            return HttpResponse(self.data, content_type="application/json")
        else:
            return render(request, self.template_403)


class BaseListarValores(ListView):
    """ LISTAR INFORMACIÓN PERTENECIENTE A UN MODELO SERIALIZANDO MANUALMENTE.

    Su función es mostrar un listado de los registros pertenecientes al modelo en cuestión que se desea utilizar.

    Variables:
    -- model                        : modelo a utilizarse.
    -- queryset                     : consulta a realizarse.
    -- data_usuario                 : datos de consulta serializados en formato JSON.
    -- template_403                 : template que renderiza el error 403 de acción prohibida.

    Metodos:
    -- get                          : método a ejecutarse que retornará todos los datos pertenecientes al modelo alojado en la variable
                                      -- model -- obtenidos a través de la variable -- queryset -- en formato JSON.

                                      Todo esto se lleva a cabo si la petición ha sido enviada a través de una solicitud AJAX,
                                      en caso no sea así se mostrará un template de error 403 FORBIDDEN.


    """
    model = None
    data = None
    template_403 = '403.html'

    def get_queryset(self):
        return list(self.model.objects.filter(estado=True).values())

    def get(self, request, modelos, *args, **kwargs):
        if request.is_ajax():
            self.model = modelos
            self.data = self.get_queryset()
            temp_gene = []
            for temp in self.data:
                temp_data = []
                for temp2 in temp:
                    temp_lis = {}
                    temp_lis['{0}'.format(temp2)] = str(temp[temp2])
                    temp_data.append(temp_lis)
                temp_gene.append(temp_data)
            self.data = json.dumps(temp_gene)
            return HttpResponse(self.data, content_type="application/json")
        else:
            return render(request, self.template_403)


class BaseActualizar(UpdateView):
    """ ACTUALIZAR UNA INSTANCIA DE UN MODELO.

    Su función es actualizar en la base de datos una instancia de un modelo en cuestión,
    dicho modelo es pasado por parámetro a través del método post redefinido en la clase.

    Variables:
    -- model                        : modelo a utilizarse.
    -- data                         : datos de la instancia en cuestión.
    -- template_403                 : template que renderiza el error 403 de acción prohibida.

    Metodos:
    -- post                         : método a ejecutarse que actualizará la instancia de un modelo.
                                      El método asigna el modelo enviado por parámetro al modelo de la clase
                                      para luego verificar si existen campos de tipo Booleanos enviados desde el
                                      frontend, tomando como diccionario el contenido y devolviendolo validado,
                                      luego de ello se registra una nueva instancia de un Form perteneciente al modelo
                                      que se está trabajando, esto a través del método --modelform_factory -- definiendo
                                      que tome todos los parámetros de este modelo, luego se le asigna la información
                                      que ya ha sido validada en el paso anterior para que Django asigne automaticamente
                                      cada campo a su correspondiente atributo para posteriormente validar este Form y
                                      proceder a guardar en la base de datos la información actualizada, retornando una
                                      instancia de JsonResponse con un mensaje de éxito y el código HTTP 201 CREATED.

                                      En caso la información asignada al Form no sea válida, se devuelve una instancia de
                                      JsonResponse con el mensaje de error y los errores que el Form ha detectado y generado
                                      junto con el códgo HTTP 400 BAD REQUEST.

                                      Todo esto se lleva a cabo si la petición ha sido enviada a través de una solicitud AJAX,
                                      en caso no sea así se mostrará un template de error 403 FORBIDDEN.

    -- get                           : método que retorna la información de la instancia en cuestión solo si la petición se
                                       ha realizado vía AJAX, en caso contrario se mostrará un template de error 404 FORBIDDEN.


    """
    model = None
    data = None
    template_403 = '403.html'

    def get(self, request, modelos, *args, **kwargs):
        if request.is_ajax():
            self.model = modelos
            self.object = self.get_object()
            self.data = model_to_dict(self.object)
            self.data = serialize('json', [
                                  self.object, ], use_natural_foreign_keys=True, use_natural_primary_keys=True)
            #self.data = json.dumps(self.data)
            return HttpResponse(self.data, content_type="application/json")
        else:
            return render(request, self.template_403)

    def post(self, request, modelos, form, *args, **kwargs):
        if request.is_ajax():
            self.model = modelos
            request.POST._mutable = True
            request.POST['estado'] = True
            data = request.POST
            data = convertir_booleanos(data)
            formulario = modelform_factory(model=self.model, form=form)
            formulario = formulario(data, instance=self.get_object())
            if formulario.is_valid():
                formulario.save()
                mensaje = "{0} actualizado correctamente!".format(
                    self.model.__name__)
                error = 'Ninguno'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = "{0} no se ha podido actualizar!".format(self.model)
                error = formulario.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return render(request, self.template_403)


class BaseEliminarLogico(DeleteView):
    """ ELIMINAR LÓGICAMENTE UNA INSTANCIA DE UN MODELO.

    Su función es eliminar lógicamente en la base de datos una instancia de un modelo en cuestión,
    dicho modelo es pasado por parámetro a través del método post redefinido en la clase.

    Variables:
    -- model                        : modelo a utilizarse.
    -- data                         : datos de la instancia en cuestión.
    -- template_403                 : template que renderiza el error 403 de acción prohibida.

    Metodos:
    -- post                         : método a ejecutarse que eliminará lógicamente una instancia de un modelo, esto lo hará
                                      convirtiendo en un diccionario la información de la instancia en cuestión a través de
                                      la función -- model_to_dict -- para luego verificar si existe el atributo llamado
                                      -- estado -- en dicho modelo el cuál será tomado para cambiar su valor a False,
                                      desactivando lógicamente dicha instancia y haciendo que no sea visible.
                                      Luego se retorna una instancia de JsonResponse con un mensaje de éxito y el código
                                      HTTP 200 OK.
                                      En caso no se encuentre el atributo -- estado -- se retorna una instancia de JsonResponse
                                      con un mensaje de error mencionando que no existe tal atributo y el código HTTP 400 BAD REQUEST.

                                      Todo esto se lleva a cabo si la petición ha sido enviada a través de una solicitud AJAX,
                                      en caso no sea así se mostrará un template de error 403 FORBIDDEN.

    -- get                           : método que retorna la información de la instancia en cuestión solo si la petición se
                                       ha realizado vía AJAX, en caso contrario se mostrará un template de error 404 FORBIDDEN.


    """
    model = None
    data = None
    template_403 = '403.html'

    def get(self, request, modelos, *args, **kwargs):
        if request.is_ajax():
            self.model = modelos
            self.object = self.get_object()
            self.data = model_to_dict(self.object)
            return JsonResponse(self.data)
        else:
            return render(request, self.template_403)

    def post(self, request, modelos, *args, **kwargs):
        if request.is_ajax():
            self.model = modelos
            self.object = self.get_object()
            self.data = model_to_dict(self.object)
            self.object.estado = False
            self.object.save()
            mensaje = "{0} eliminado correctamente!".format(self.object)
            error = 'Ninguno'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 200
            return response
        else:
            return render(request, self.template_403)


class Inicio(CreateView):
    pass


class Actualizar(TemplateView):
    pass
