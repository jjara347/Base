from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from aplicaciones.base.models import ModeloBase
from aplicaciones.base.utils import obtener_modelo
from aplicaciones.usuarios.models import Usuario


class Empresa(ModeloBase):
    EmEmp_Nombre = models.CharField(
        blank=False, max_length=100, verbose_name='Nombre')


    class Meta:
        db_table = 'EmEmp_Empresa'

    def natural_key(self):
        return (self.EmEmp_Nombre)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return self.EmEmp_Nombre


class EmpresaSeleccionada(ModeloBase):
    ESd_Nombre = models.CharField(blank=False, null=True,
                              max_length=100, verbose_name='Nombre')
    ESd_Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ESd_EmpresaSeleccionada'

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return self.ESd_Nombre


class Grupo(ModeloBase):
    GmGru_Name = models.CharField(
        'Nombre de Grupo', max_length=80, unique=True)
    GmGru_Permissions = models.ManyToManyField(Permission)


    class Meta:
        db_table = 'GmGru_Grupo'

    def natural_key(self):
        return (self.GmGru_Name)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return self.GmGru_Name


class Item(ModeloBase):
    ImItm_Nombre = models.CharField('Nombre de Item', max_length = 100, unique = True)
    ImItm_Url = models.CharField('Url de Item', max_length = 200, unique = True,blank = True)
    ImItm_Icono = models.CharField('Nombre de Icono de FontAwesome', max_length=100, blank = True)
    ImItm_GrupoPermisos = models.ManyToManyField(Grupo)

    def natural_key(self):
        return (self.ImItm_Nombre)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        db_table = 'ImItm_Item'
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


    def get_grupos(self):
        return ",".join([str(grupo) for grupo in self.ImItm_GrupoPermisos.all()])

    def __str__(self):
        return self.ImItm_Nombre

    def save(self,*args,**kwargs):        
        if not self.id:
            nuevo_grupo, creado = Grupo.objects.get_or_create(
                GmGru_Name='{0}'.format(self.ImItm_Nombre))
            self.ImItm_Url = '/{0}/'.format(
                self.ImItm_Nombre.replace(' ', '_').lower())
            permisos_defecto = ['add','change','delete','view']
            for permiso in permisos_defecto:
                try:
                    per = Permission.objects.create(
                                        name = 'Can {0} {1}'.format(permiso,self.ImItm_Nombre),
                                        content_type = ContentType.objects.get_for_model(Item),
                                        codename='{0}_{1}'.format(permiso, self.ImItm_Nombre)
                                        )
                    if creado:
                        nuevo_grupo.GmGru_Permissions.add(per)
                except:
                    raise ValidationError(
                        _('Ha sucedido un error en la creación de los permisos para la instancia {0} del modelo {1}'.format(
                            self.ImItm_Nombre, Item.__name__)),
                    )
            super(Item,self).save(*args,**kwargs)
            self.ImItm_GrupoPermisos.add(nuevo_grupo)
        else:
            datos_anteriores = Item.objects.get(id = self.id)
            self.ImItm_Url = '/{0}/'.format(
                self.ImItm_Nombre.replace(' ', '_').lower())
            if self.ImItm_Nombre == datos_anteriores.ImItm_Nombre:
                super(Item,self).save(*args,**kwargs)
            else:
                antiguo_grupo = Grupo.objects.get(
                    GmGru_Name='{0}'.format(datos_anteriores.ImItm_Nombre))
                self.ImItm_Url = '/{0}/'.format(
                    self.ImItm_Nombre.replace(' ', '_').lower())
                super(Item,self).save(*args,**kwargs)
                antiguo_grupo.GmGru_Name = 'temp_{0}'.format(
                    antiguo_grupo.GmGru_Name)
                antiguo_grupo.save()
                nuevo_grupo_a_crear = Grupo.objects.create(
                    GmGru_Name='{0}'.format(self.ImItm_Nombre))
                nuevo_grupo_a_crear.GmGru_Permissions.set(
                    antiguo_grupo.permissions.all())
                antiguo_grupo.delete()
                permisos_defecto = ['add','change','delete','view']
                for permiso in permisos_defecto:
                    try:
                        per = Permission.objects.get(
                            codename='{0}_{1}'.format(
                            permiso, datos_anteriores.ImItm_Nombre)
                            ).delete()
                    except:
                        raise ValidationError(
                            _('Ha sucedido un error en la eliminación de los permisos para la instancia {0} del modelo {1}'.format(
                                self.ImItm_Nombre, Item.__name__)),
                        )
                    try:
                        per = Permission.objects.create(
                                            name='Can {0} {1}'.format(permiso, self.ImItm_Nombre),
                                            content_type = ContentType.objects.get_for_model(Item),
                                            codename = '{0}_{1}'.format(permiso,self.ImItm_Nombre)
                                            )
                        nuevo_grupo_a_crear.GmGru_Permissions.add(per)
                    except:
                        raise ValidationError(
                            _('Ha sucedido un error en la creación de los permisos para la instancia {0} del modelo {1}'.format(
                                self.ImItm_Nombre, Item.__name__)),
                        )

@receiver(post_save,sender=Item)
def asignar_grupo(sender,**kwargs):
    item = Item.objects.latest('fecha_creacion')
    grupo = Grupo.objects.filter(GmGru_Name=item.ImItm_Nombre)
    if len(grupo) != 0:
        if item.fecha_creacion == grupo[0].fecha_creacion:
            item.ImItm_GrupoPermisos.add(grupo[0])
    else:
        item = Item.objects.latest('fecha_modificacion')
        grupo = Grupo.objects.filter(GmGru_Name=item.ImItm_Nombre)
        if grupo:
            item.ImItm_GrupoPermisos.add(grupo[0])




class SubItem(ModeloBase):
    SId_ItemPadre = models.ForeignKey(Item,on_delete = models.CASCADE)
    SId_Modelo = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    SId_Nombre = models.CharField('Nombre de Modelo Enlazado', max_length = 100, unique = False, blank = True)
    SId_Url = models.CharField('Url de SubItem', max_length = 200, unique = True,blank = True)    

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        db_table = 'SId_SubItem'
        verbose_name = 'Sub Item'
        verbose_name_plural = 'Subs Items'

    def save(self,*args,**kwargs):
        if not self.id:
            self.SId_Nombre = obtener_modelo(
                self.SId_Modelo.app_label, self.SId_Modelo.model).__name__
            self.SId_Url = '/{0}{1}{2}/'.format(
                self.SId_Modelo.app_label, self.SId_ItemPadre.ImItm_Url, self.SId_Nombre.lower())
            permisos_defecto = ['add','change','delete','view']
            grupo = Grupo.objects.get(
                GmGru_Name=self.SId_ItemPadre.ImItm_Nombre)
            for permiso in permisos_defecto:
                try:
                    perm,creado = Permission.objects.get_or_create(
                                        name = 'Can {0} {1}'.format(permiso,self.SId_Nombre),
                                        content_type = ContentType.objects.get_for_model(Item),
                                        codename='{0}_{1}'.format(permiso, self.SId_Nombre)
                                        )
                    if creado:
                        grupo.GmGru_Permissions.add(perm)
                except:
                    raise ValidationError(
                        _('Ha sucedido un error en la creación de los permisos para la instancia {0} del modelo {1}'.format(
                            self.SId_Nombre, SubItem.__name__)),
                    )
            super(SubItem,self).save(*args,**kwargs)
        else:
            datos_anteriores = SubItem.objects.get(id = self.id)
            self.SId_Url = '/{0}{1}{2}/'.format(self.SId_Modelo.app_label,
                                            self.SId_ItemPadre.ImItm_Url, self.SId_Nombre.lower())
            if self.SId_Nombre == datos_anteriores.SId_Nombre:
                super(SubItem,self).save(*args,**kwargs)
            else:
                permisos_defecto = ['add','change','delete','view']
                for permiso in permisos_defecto:
                    try:
                        Permission.objects.get(
                                codename='{0}_{1}'.format(
                                permiso, datos_anteriores.SId_Nombre)
                                ).delete()
                    except:
                        raise ValidationError(
                            _('Ha sucedido un error en la eliminación de los permisos para la instancia {0} del modelo {1}'.format(
                                self.SId_Nombre, SubItem.__name__)),
                        )
                    try:
                        Permission.objects.create(
                                            name = 'Can {0} {1}'.format(permiso,self.SId_Nombre),
                                            content_type = ContentType.objects.get_for_model(Item),
                                            codename='{0}_{1}'.format(permiso, self.SId_Nombre)
                                            )
                    except:
                        raise ValidationError(
                            _('Ha sucedido un error en la creación de los permisos para la instancia {0} del modelo {1}'.format(
                                self.SId_Nombre, SubItem.__name__)),
                        )
                super(SubItem,self).save(*args,**kwargs)

    def __str__(self):
        return self.SId_Nombre

class Menu(ModeloBase):
    MmMen_Usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    MmMen_Empresa = models.ForeignKey(Empresa,on_delete = models.CASCADE, null = True, blank = True)
    MmMen_Item = models.ManyToManyField(Item)

    class Meta:
        db_table = 'MmMen_Menu'

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def clean(self):
        if not self.id:
            menu_exists, creado = Menu.objects.get_or_create(
                MmMen_Usuario=self.MmMen_Usuario, MmMen_Empresa=self.MmMen_Empresa)
            if not creado:
                mensaje = f"Ya existe un Menu con : { self.MmMen_Usuario } asociado a la empresa : { self.MmMen_Empresa }"
                raise ValidationError(mensaje)
            else: menu_exists.delete()
        else:        
            pass

    def __str__(self):
        return 'Menú {0}'.format(self.id)
