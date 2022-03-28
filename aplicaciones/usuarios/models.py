from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UsuarioManager(BaseUserManager):
    def create_user(self, UmUsr_Email, UmUsr_Username, UmUsr_Nombres, UmUsr_Apellidos, password=None):
        """ Creación de un usuario.

        Retorna un usuario creado y guardado en la base de datos, con la información
        recibida

        Parámetros:
        UmUsr_Email -- correo que tendrá el usuario, debe ser único.
        UmUsr_Nombres -- nombres del usuario.
        UmUsr_Apellidos -- apellidos del usuario.
        password -- contraseña sin encriptar.

        """
        if not UmUsr_Email:
            raise ValueError('El usuario debe tener un correo electrónico!')

        user = self.model(
            UmUsr_Username=UmUsr_Username,
            UmUsr_Email=self.normalize_email(UmUsr_Email),
            UmUsr_Nombres=UmUsr_Nombres,
            UmUsr_Apellidos=UmUsr_Apellidos,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, UmUsr_Username, UmUsr_Email, UmUsr_Nombres, UmUsr_Apellidos, password):
        """ Creación de un superusuario.

        Retorna un superusuario creado y guardado en la base de datos, con la información
        recibida y los permisos completos.

        Parámetros:
        UmUsr_Email -- correo que tendrá el usuario, debe ser único.
        UmUsr_Nombres -- nombres del usuario.
        UmUsr_Apellidos -- apellidos del usuario.
        password -- contraseña sin encriptar.

        """
        user = self.create_user(
            UmUsr_Email,
            UmUsr_Username=UmUsr_Username,
            password=password,
            UmUsr_Nombres=UmUsr_Nombres,
            UmUsr_Apellidos=UmUsr_Apellidos,
        )
        user.UmUsr_UsuarioAdministrador = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    UmUsr_Username = models.CharField(max_length=255, unique=True)
    UmUsr_Email = models.EmailField(
        'Correo Electrónico', max_length=255, unique=True,)
    UmUsr_Nombres = models.CharField(
        'Nombres', max_length=255, blank=True, null=True)
    UmUsr_Apellidos = models.CharField(
        'Apellidos', max_length=255, blank=True, null=True)
    UmUsr_UsuarioActivo = models.BooleanField(default=True)
    UmUsr_UsuarioAdministrador = models.BooleanField(default=False)
    objects = UsuarioManager()

    class Meta:
        db_table = 'UmUsr_Usuario'

    USERNAME_FIELD = 'UmUsr_Username'
    REQUIRED_FIELDS = ['UmUsr_Email', 'UmUsr_Nombres', 'UmUsr_Apellidos']

    def natural_key(self):
        return (self.UmUsr_Username)

    def __str__(self):
        """ Visualización por defecto de un modelo.

        Retorna un formato de visualización por defecto de una instancia de un modelo, en este
        caso del modelo Usuario, este formato será visible cuando se desee visualizar tanto en
        navegador, consola, o en cualquier lugar que sea llamado.

        """
        return "Usuario {0}, con Nombre Completo: {1} {2}".format(self.UmUsr_Username, self.UmUsr_Apellidos, self.UmUsr_Nombres)

    def has_perm(self, perm, obj=None):
        "Respuesta a permiso"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Respues a permisos para vista por parte del usuario."
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Retorna si usuario es un superusuario."
        # Simplest possible answer: All admins are staff
        return self.UmUsr_UsuarioAdministrador
