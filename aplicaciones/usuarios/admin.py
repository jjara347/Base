from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.contenttypes.models import ContentType
from aplicaciones.usuarios.models import Usuario


class FormularioCreacionUsuario(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Contraseña de Confirmación', widget = forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('UmUsr_Username', 'UmUsr_Email',
                  'UmUsr_Nombres', 'UmUsr_Apellidos')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Contraseñas no coinciden!")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class FormularioEdicionUsuario(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('UmUsr_Username', 'UmUsr_Email', 'password', 'UmUsr_Nombres',
                  'UmUsr_Apellidos', 'UmUsr_UsuarioActivo', 'UmUsr_UsuarioAdministrador')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UsuarioAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = FormularioEdicionUsuario
    add_form = FormularioCreacionUsuario

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('UmUsr_Username', 'UmUsr_Email', 'UmUsr_Nombres',
                    'UmUsr_Apellidos', 'UmUsr_UsuarioActivo', 'UmUsr_UsuarioAdministrador')
    list_filter = ('UmUsr_UsuarioAdministrador',)
    fieldsets = (
        (None, {'fields': ('UmUsr_Username', 'UmUsr_Email', 'password')}),
        ('Información Personal', {'fields': ('UmUsr_Nombres', 'UmUsr_Apellidos',)}),
        ('Permisos', {
         'fields': ('UmUsr_UsuarioAdministrador', 'UmUsr_UsuarioActivo')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('UmUsr_Email', 'UmUsr_Nombres', 'UmUsr_Apellidos', 'password1', 'password2')}
        ),
    )
    search_fields = ('UmUsr_Email',)
    ordering = ('UmUsr_Email',)
    filter_horizontal = ()

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('codename','name','content_type')
    search_fields = ('codename','name',)

# Now register the new UserAdmin...
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(ContentType)
admin.site.register(Permission,PermissionAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
