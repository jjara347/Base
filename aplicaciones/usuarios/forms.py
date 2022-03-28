from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class FormularioCreacionUsuario(forms.ModelForm):
    """ Formulario de Registro de un Usuario en la Base de datos.

    Form de Django basado en el modelo Usuario que contiene la información necesaria
    para que Django cree el HTML correspondiente a cada atributo del modelo Autor.

    """
    #username = forms.CharField(label = 'Nombre de Usuario', widget = forms.TextInput)
    #email = forms.EmailField(label = 'Correo Electrónico',widget = forms.TextInput)
    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese su Contraseña...',
            'id':'password1',
            'required':'required'
        }
    ))
    password2 = forms.CharField(label = 'Contraseña de Confirmación', widget = forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese su Contraseña otra vez...',
            'id':'password2',
            'required':'required'
        }
    ))

    class Meta:
        model = Usuario
        fields = ('UmUsr_Email', 'UmUsr_Nombres',
                  'UmUsr_Apellidos', 'UmUsr_Username')
        widgets = {
            'UmUsr_Email': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Correo Electrónico',
                    'id': 'UmUsr_Email',
                    'required':'required'
                }
            ),
            'UmUsr_Nombres': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Nombres',
                    'id': 'UmUsr_Nombres',
                    'required':'required'
                }
            ),
            'UmUsr_Apellidos': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Apellidos',
                    'id': 'UmUsr_Apellidos',
                    'required':'required'
                }
            ),
            'UmUsr_Username': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Nombre de Usuario',
                    'id': 'UmUsr_Username',
                    'required':'required'
                }
            )
        }

    def clean_password2(self):
        """ Validación de contraseña.

        Método que valida que ambas contraseñas ingresadas sean iguales antes de ser encriptadas y guardadas
        en la Base de datos. Retorna la contraseña válida.

        Excepciones:
        ValidationError -- cuando las contraseñas no son iguales muestra un mensaje de error.


        """
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Contraseñas no coinciden!")
        return password2

    def clean_UmUsr_Username(self):
        """ Validación de nombres.

        Método que valida que el campo nombres ingresado sea correcto. Retorna los nombres válidos.

        Excepciones:
        ValidationError -- cuando el campo es dejado en blanco.

        """
        nombres = self.cleaned_data['UmUsr_Nombres']
        if nombres is None:
            raise forms.ValidationError("El campo Nombres es obligatorio!")
        return nombres

    def clean_UmUsr_Apellidos(self):
        """ Validación de apellidos.

        Método que valida que el campo apellidos ingresado sea correcto. Retorna los apellidos válidos.

        Excepciones:
        ValidationError -- cuando el campo es dejado en blanco.

        """
        apellidos = self.cleaned_data['UmUsr_Apellidos']
        if apellidos is None:
            raise forms.ValidationError("El campo Apellidos es obligatorio!")
        return apellidos

    def clean_UmUsr_Email(self):
        """ Validación de email.

        Método que valida que el campo email ingresado sea correcto. Retorna el email válidos.

        Excepciones:
        ValidationError -- cuando el campo es dejado en blanco.

        """
        email = self.cleaned_data['UmUsr_Email']
        if email is None:
            raise forms.ValidationError("El campo Email es obligatorio!")
        return email

    def clean_UmUsr_Username(self):
        """ Validación de username.

        Método que valida que el campo username ingresado sea correcto. Retorna el username válidos.

        Excepciones:
        ValidationError -- cuando el campo es dejado en blanco.

        """
        username = self.cleaned_data['UmUsr_Username']
        if username is None:
            raise forms.ValidationError("El campo Nombre de Usuario es obligatorio!")
        return username

    def save(self, commit=True):
        """ Registro en la base de datos.

        Invoca al método save() del modelo Usuario el cuál invoca al ORM de Django para que
        ejecute el insert into correspondiente al modelo indicado enviandole la información
        correspondiente, antes de ello, se encripta la contraseña para su protección.
        Retorna la instancia del usuario registrado.

        """
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
        fields = ('UmUsr_Email', 'UmUsr_Nombres',
                  'UmUsr_Apellidos', 'UmUsr_Username')
        widgets = {
            'UmUsr_Email': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'required':'required',
                }
            ),
            'UmUsr_Nombres': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'required':'required'
                }
            ),
            'UmUsr_Apellidos': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'required':'required'
                }
            ),
            'UmUsr_Username': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'required':'required'
                }
            )
        }
