import json
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView
from django.http import JsonResponse, HttpResponse
from aplicaciones.menu.models import Menu as Men, Item, SubItem, EmpresaSeleccionada, Empresa
from aplicaciones.menu.forms import *


class Empresas(ListView):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            empresas = Men.objects.filter(estado=True, MmMen_Usuario=request.user).values(
                'MmMen_Empresa__EmEmp_Nombre', 'MmMen_Empresa__id')
            data = []
            for em in empresas:
                lista = {}
                lista['nombre'] = em['MmMen_Empresa__EmEmp_Nombre']
                lista['id'] = em['MmMen_Empresa__id']
                data.append(lista)
            data = json.dumps(data)
            return HttpResponse(data, content_type="application/json")


class EmpresaInicial(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            empresa_inicial = EmpresaSeleccionada.objects.filter(
                estado=True, ESd_Usuario=request.user).values('ESd_Nombre')
            try:
                id_empresa_inicial = Empresa.objects.get(
                    ESd_Nombre=empresa_inicial[0]['ESd_Nombre'])
                data = []
                lista = {}
                lista['ESd_Nombre'] = empresa_inicial[0]['ESd_Nombre']
                lista['id'] = id_empresa_inicial.id
                data.append(lista)
                data = json.dumps(data)
                return HttpResponse(data)
            except:
                temporal_empresa = Men.objects.filter(
                    estado=True,
                    MmMen_Usuario=request.user
                ).values('MmMen_Empresa__EmEmp_Nombre')[:1]
                empresa_inicial = EmpresaSeleccionada(
                    ESd_Nombre=temporal_empresa[0]['MmMen_Empresa__EmEmp_Nombre'],
                    ESd_Usuario=request.user
                )
                empresa_inicial.save()
                id_empresa_inicial = Empresa.objects.get(
                    EmEmp_Nombre=empresa_inicial.ESd_Nombre)
                data = []
                lista = {}
                lista['ESd_Nombre'] = empresa_inicial.ESd_Nombre
                lista['id'] = id_empresa_inicial.id
                data.append(lista)
                data = json.dumps(data)
                return HttpResponse(data)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            temp_selec = Empresa.objects.get(id=request.POST.get('id'))
            emp_selec = EmpresaSeleccionada.objects.get(
                estado=True, ESd_Usuario=request.user)
            emp_selec.ESd_Nombre = temp_selec.EmEmp_Nombre
            emp_selec.save()
            return HttpResponse(request.POST.get('id'))


class ObtenerMenu(View):
    def get(self, request, id, *args, **kwargs):
        if request.is_ajax():
            try:
                queryset = Men.objects.filter(
                    estado=True, MmMen_Usuario=request.user, MmMen_Empresa=Empresa.objects.get(id=id, estado=True))
                menu = ''
                for query in queryset:
                    for item in query.MmMen_Item.all():
                        menu += '<ul class="pcoded-item pcoded-left-item">'
                        menu += '<li class="pcoded-hasmenu"><a>'
                        menu += '<span class="pcoded-micon"><i class="{0}"></i></span>'.format(
                            item.ImItm_Icono)
                        menu += '<span class="pcoded-mtext">{0}</span></a>'.format(
                            item.ImItm_Nombre)
                        menu += '<ul class="pcoded-submenu">'
                        temp_subitem = SubItem.objects.filter(
                            SId_ItemPadre=item.id)
                        for temp in temp_subitem:
                            menu += '<li class=""><a href="{0}">'.format(
                                temp.SId_Url)
                            menu += '<span class="pcoded-mtext">{0}</span>'.format(
                                temp.SId_Nombre)
                            menu += '</a></li>'
                        menu += '</ul>'
                        menu += '</li>'
                        menu += '</ul>'
                return HttpResponse(menu)
            except ValueError as e:
                return HttpResponse(e)



