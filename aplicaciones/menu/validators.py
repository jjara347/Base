def validarMenuUsuarioAdministrador(request, nombre):
    if (nombre == 'Mantenimiento' or nombre == 'Usuarios') and request.user.is_staff:
        return True
    else:
        return False


def validarMenuPrivado(usuario, nombre):
    if ('mantenimiento' in nombre.lower() or 'usuarios' in nombre.lower()) and not usuario.is_staff:
        return True
    else:
        return False
