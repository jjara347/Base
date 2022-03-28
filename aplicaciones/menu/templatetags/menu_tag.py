from django import template
from django.http import HttpResponse
from aplicaciones.menu.models import Menu,SubItem,Item

register = template.Library()

@register.simple_tag
def obtenerMenu():
    queryset = Menu.objects.filter(estado = True)
    return queryset

@register.simple_tag
def obtenerSubitems():
    queryset = Menu.objects.filter(estado = True)
    prueba = []
    menu = ''
    for query in queryset:
        for item in query.MmMen_Item.all():
            prueba.append(
                [p for p in SubItem.objects.filter(SId_ItemPadre=item.id)])
    """
    for subitem in prueba:
        for subsubitem in subitem:
            menu += '<div id="{0}" class="tab-pane notika-tab-menu-bg animated flipInX">'.format(subsubitem.nombre.lower())
            menu += '<ul class="notika-main-menu-dropdown">'
            menu += '<li><a href="{0}"><i class="{1}"></i>&nbsp;{2}</a></li>'.format(subsubitem.url,subsubitem.icono,subsubitem.nombre)
            menu += '</ul>'
            menu += '</div>'
            menu += '</div>'
    """
    return prueba
