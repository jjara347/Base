from django.contrib import admin
from django.db.models import Q
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
#from jet.filters import RelatedFieldAjaxListFilter
from aplicaciones.menu.models import *
from aplicaciones.usuarios.models import Usuario

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('ImItm_Nombre', 'ImItm_Icono',)

def delete_items_permisos(modeladmin, request,queryset):
    for item in queryset:
        permisos_defecto = ['add','change','delete','view']
        for permiso in permisos_defecto:
            try:
                Permission.objects.get(codename='{0}_{1}'.format(permiso, item.ImItm_Nombre)).delete()
            except:
                raise ValidationError(
                    _('Ha sucedido un error en la eliminación de los permisos para la instancia {0} del modelo {1}'.format(
                        self.ImItm_Nombre, Item.__name__)),
                )
        item.delete()
delete_items_permisos.short_description = "Eliminar Items incluyendo sus Permisos"

def delete_items(modeladmin,request,queryset):
    for item in queryset:
        item.delete()

delete_items.short_description = "Eliminar sólo Items"

def delete_items_permisos_grupos(modeladmin, request,queryset):
    for item in queryset:
        permisos_defecto = ['add','change','delete','view']
        for permiso in permisos_defecto:
            try:
                Permission.objects.get(
                    codename='{0}_{1}'.format(permiso, item.ImItm_Nombre)
                                    ).delete()
            except:
                raise ValidationError(
                    _('Ha sucedido un error en la eliminación de los permisos para la instancia {0} del modelo {1}'.format(
                        self.ImItm_Nombre, Item.__name__)),
                )
        for grupo in item.ImItm_GrupoPermisos.all():
            grupo.delete()
        item.delete()
delete_items_permisos_grupos.short_description = "Eliminar Items incluyendo sus Permisos y Grupos Asignados"

class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    search_fields = ('ImItm_Nombre',)
    list_display = ('ImItm_Nombre', 'ImItm_Url', 'ImItm_Icono', 'get_grupos',)
    actions = [delete_items,delete_items_permisos,delete_items_permisos_grupos,]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class SubItemForm(forms.ModelForm):
    class Meta:
        model = SubItem
        fields = ('SId_ItemPadre', 'SId_Modelo')

    def __init__(self,*args,**kwargs):
        super(SubItemForm,self).__init__(*args,**kwargs)
        try:
            self.fields['SId_Modelo'].queryset = ContentType.objects.exclude(
                Q(model='logentry') |
                Q(model='permission') |
                Q(model='group') |
                Q(model='contenttype') |
                Q(model='session') |
                Q(model__icontains='historical') |
                Q(model__icontains='bookmark') |
                Q(model__icontains='dashboard') |
                Q(model__icontains='pinnedapplication') |
                Q(model__icontains="logentry")
            )
        except (AttributeError, ObjectDoesNotExist):
            pass


class SubItemAdmin(admin.ModelAdmin):
    form = SubItemForm
    search_fields = ('SId_Nombre',)
    list_display = ('SId_Nombre', 'SId_Url', 'SId_ItemPadre')

class EmpresaAdmin(admin.ModelAdmin):
    search_fields = ('EmEmp_Nombre',)
    list_display = ('id', 'EmEmp_Nombre', 'estado', 'fecha_creacion')

admin.site.register(Item,ItemAdmin)
admin.site.register(SubItem,SubItemAdmin)
admin.site.register(Grupo)
admin.site.register(Menu)
admin.site.register(Empresa,EmpresaAdmin)
admin.site.register(EmpresaSeleccionada)
