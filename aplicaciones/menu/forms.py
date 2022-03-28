from django import forms
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from aplicaciones.menu.models import Menu, Empresa, Item, SubItem
from aplicaciones.menu.validators import validarMenuPrivado


class MenuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['MmMen_Usuario'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['MmMen_Empresa'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['MmMen_Empresa'].queryset = Empresa.objects.filter(
            estado=True)
        self.fields['MmMen_Item'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = Menu
        fields = '__all__'

    def clean_item(self):
        items = self.cleaned_data['MmMen_Item']
        usuario = self.cleaned_data['MmMen_Usuario']
        for item in items:
            if validarMenuPrivado(usuario, item.ImItm_Nombre):
                raise ValidationError(
                    _('Item no se puede añadir debido a que el Usuario no es un Usuario Administrador'), code='invalid')
        return items


class EmpresaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['EmEmp_Nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['nomEmEmp_Nombrebre'].widget.attrs.update(
            {'placeholder': 'Ingrese el nombre de la empresa...'})

    class Meta:
        model = Empresa
        fields = '__all__'


class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ImItm_Nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['ImItm_Nombre'].widget.attrs.update(
            {'placeholder': 'Ingrese el nombre del item...'})
        self.fields['ImItm_Icono'].widget.attrs.update({'class': 'form-control'})
        self.fields['ImItm_Icono'].widget.attrs.update(
            {'placeholder': 'Ingrese el nombre del icono de FontAwesome'})

    class Meta:
        model = Item
        fields = ('ImItm_Nombre', 'ImItm_Icono')


class SubItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['SId_ItemPadre'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['SId_Modelo'].widget.attrs.update(
            {'class': 'form-control'})
        try:
            self.fields['SId_Modelo'].queryset = ContentType.objects.exclude(
                Q(model='logentry') |
                Q(model='session') |
                Q(model__icontains='historical') |
                Q(model__icontains='bookmark') |
                Q(model__icontains='dashboard') |
                Q(model__icontains='pinnedapplication') |
                Q(model__icontains="logentry")
            )
        except (AttributeError, ObjectDoesNotExist):
            pass

    class Meta:
        model = SubItem
        fields = ('SId_ItemPadre', 'SId_Modelo')
