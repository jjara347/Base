import json
from django.shortcuts import render,get_object_or_404
from django.views.generic import View,DeleteView,UpdateView,TemplateView
from django.http import JsonResponse
from django.http import HttpResponseRedirect,HttpResponse
from django.apps import apps
from aplicaciones.base.base_reportes import FormatoReporteExcel
from aplicaciones.usuarios.forms import FormularioCreacionUsuario,FormularioEdicionUsuario
from aplicaciones.usuarios.models import Usuario

class InicioUsuario(View):
    template_name = 'usuarios/index_usuarios.html'

    def post(self,request,*args,**kwargs):
        """ Lógica cuando la petición HTTP enviada por el navegador es POST.

        Valida que la petición halla sido enviada por un usuario logueado y válido,
        además de que la petición se halla hecho vía AJAX. Luego se obtiene la instancia
        del Form de Django perteneciente a dicho modelo para obtener la información enviada
        del navegador, se valida esta información, lo que puede dar 2 posibilidades:

            - SE ACEPTA:entonces se procede a registrar esta información
                        en la base de datos en caso sea válida, para luego responder una instancia de la
                        clase JsonResponse, la cuál es una de las maneras optimas que Django ofrece para
                        responder en formato Json errores o mensajes al navegador, además de indicar el
                        status_code que indica el estado de la respuesta según los estándares HTTP.
            - SE RECHAZA:entonces se procede a instanciar JsonResponse indicandole un mensaje de error
                         junto con todos los errores que el Form de Django correspondiente al Usuario
                         ha detectado, así del status_code correspondiente.

        """
        if request.user.is_authenticated:
            if request.is_ajax():
                formulario = FormularioCreacionUsuario(request.POST or None)
                if formulario.is_valid():
                    formulario.save()
                    response = JsonResponse({"mensaje":"Usuario registrado correctamente!"})
                    response.status_code = 201
                    return response
                else:
                    response = JsonResponse({"error":"Ha ocurrido un error","mensaje":formulario.errors,"length":len(formulario.errors)})
                    response.status_code = 403
                    return response
        return render(request,self.template_name)


    def get(self,request,*args,**kwargs):
        """Lógica cuando la petición HTTP enviada por el navegador es GET.

        Verifica que la petición halla sido enviada por un usuario logueado y con los permisos
        adecuados, además que la petición sea vía AJAX, lo que da 2 posibilidades:

            - PETICIÓN AJAX: obtiene la lista de usuarios registrados y activos y lo retorna
                             vía JSON haciendo una conversión de una lista de Python a JSON.

            - PETICIÓN NO AJAX: indica que solo se desea renderizar un template, es decir que
                                se está accediendo a la ruta para cargar la pantalla correspondiente
                                por ello retorna una instancia de render() para renderizar el
                                template indicado en la variable template_name.

        """
        if request.user.is_authenticated:
            if request.is_ajax():
                usuarios = Usuario.objects.filter(UmUsr_UsuarioActivo=True)
                lista_usuarios = []
                for usuario in usuarios:
                    data_usuario = {}
                    data_usuario['id'] = usuario.id
                    data_usuario['nombres'] = usuario.UmUsr_Nombres
                    data_usuario['apellidos'] = usuario.UmUsr_Apellidos
                    data_usuario['email'] = usuario.UmUsr_Email
                    data_usuario['username'] = usuario.UmUsr_Username
                    data_usuario['usuario_administrador'] = usuario.UmUsr_UsuarioAdministrador
                    lista_usuarios.append(data_usuario)
                data = json.dumps(lista_usuarios)
                return HttpResponse(data,'application/json')
            else:
                form = FormularioCreacionUsuario()
                context = {}
                context['form'] = form
                return render(request,self.template_name,context)

class ActualizarUsuario(View):
    template_name = 'usuarios/actualizar_usuario.html'

    def post(self,request,id,*args,**kwargs):
        """ Lógica cuando la petición HTTP enviada por el navegador es POST.

        Valida que la petición halla sido enviada por un usuario logueado y válido,
        además de que la petición se halla hecho vía AJAX. Luego se obtiene la instancia
        del Form de Django perteneciente a dicho modelo para obtener la información enviada
        del navegador, se valida esta información, lo que puede dar 2 posibilidades:

            - SE ACEPTA:entonces se procede a actualizar la información del usuario
                        en la base de datos en caso sea válida, para luego responder una instancia de la
                        clase JsonResponse, la cuál es una de las maneras optimas que Django ofrece para
                        responder en formato Json errores o mensajes al navegador, además de indicar el
                        status_code que indica el estado de la respuesta según los estándares HTTP.
            - SE RECHAZA:entonces se procede a instanciar JsonResponse indicandole un mensaje de error
                         junto con todos los errores que el Form de Django correspondiente al Usuario
                         ha detectado, así del status_code correspondiente.

        """
        usuario = get_object_or_404(Usuario,id = id)
        if request.user.is_authenticated:
            if request.is_ajax():
                formulario = FormularioEdicionUsuario(request.POST, instance = usuario)
                if formulario.is_valid():
                    nombres = formulario.cleaned_data['UmUsr_Nombres']
                    apellidos = formulario.cleaned_data['UmUsr_Apellidos']
                    email = formulario.cleaned_data['UmUsr_Email']
                    username = formulario.cleaned_data['UmUsr_Username']

                    usuario.UmUsr_Nombres = nombres
                    usuario.UmUsr_Apellidos = apellidos
                    usuario.UmUsr_Email = email
                    usuario.UmUsr_Username = username


                    usuario.save()
                    response = JsonResponse({"mensaje":"Usuario actualizado correctamente!"})
                    response.status_code = 201
                    return response
                else:
                    response = JsonResponse({"error":"Ha ocurrido un error","mensaje":formulario.errors,"length":len(formulario.errors)})
                    response.status_code = 403
                    return response
            return render(request,self.template_name)


    def get(self,request,id,*args,**kwargs):
        """Lógica cuando la petición HTTP enviada por el navegador es GET.

        Verifica que la petición halla sido enviada por un usuario logueado y con los permisos
        adecuados, además que la petición sea vía AJAX, lo que da 2 posibilidades:

            - PETICIÓN AJAX: obtiene la informaión del usuario solicitado y asocia la información
                             en una instancia del Form de edición de Usuario para ser enviada al template.

        """
        usuario = get_object_or_404(Usuario,id = id)
        if request.user.is_authenticated:
            if request.is_ajax():
                form = FormularioEdicionUsuario(instance = usuario)
                contexto = {
                    'form':form,
                }
                return render(request,self.template_name,contexto)


class EliminarUsuario(DeleteView):
    model = Usuario
    template_403 = 'administrador/403.html'

    def post(self,request,id,*args,**kwargs):
        """ Lógica de eliminación lógica cuando la petición HTTP enviada por el navegador es POST.

        Obtiene el usuario correspondiente a través del id enviado como parámetro a la función,
        cuando es obtenido se cambia el estado de su atributo usuario_activo a False y se
        procede a guardar la actualización en la base de datos, respondiendo una instancia de
        JsonResponse con un mensaje y código HTTP correcto.

        Funciones:
        get_object_or_404 -- obtiene una instancia del modelo correspondiente basada en el filtro
                             enviado como parámetro a la función en caso exista, sino retorna
                             un error 404.

        """
        if request.is_ajax():
            usuario = get_object_or_404(Usuario,id = id)
            usuario.UmUsr_UsuarioActivo = False
            usuario.save()
            response = JsonResponse(
                {"mensaje": "El Usuario {0} ha sido eliminado correctamente!".format(usuario.UmUsr_Nombres)})
            response.status_code = 200
            return response
        else:
            return render(request,self.template_403)

class ReporteUsuarioExcel(TemplateView):

    def get(self,request,*args,**kwargs):
        reporte = FormatoReporteExcel('usuarios','Usuario')
        reporte.construir_reporte()
        return reporte.obtener_reporte_excel()
