from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.apps import apps
from aplicaciones.base.forms import FormularioLogin

class Inicio(TemplateView):
    """  TEMPLATE DE INICIO.

        Retorna el template de inicio del proyecto.

    """
    template_name = 'administrador/index.html'

    def get(self,request,*args,**kwargs):
        """
        aplicaciones = apps.get_models()
        for app in aplicaciones:
            if app.__name__ != 'ContentType' and app.__name__ != 'LogEntry' and app.__name__ != 'Session' and app.__name__ != 'Permission' and app.__name__ != 'Group':
                instancias = app.objects.all()
                print("MODELO {0}, INSTANCIAS : {1}".format(app.__name__,instancias))
        """
        return render(request,self.template_name)

class Login(FormView):
    template_name = 'administrador/login.html'
    form_class = FormularioLogin
    success_url =  reverse_lazy("administrador:inicio")

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


def logoutUsuario(request):
    logout(request)
    return redirect('login')
