from django.apps import apps
from django.forms import models as mode

def obtener_consulta(modelo):
    """ OBTENER CONSULTA DE UN MODELO.

    Retorna todos los objetos junto con todos sus valores del modelo
    enviado como parámetro.

    """
    return modelo.objects.all().values()

def obtener_nombres_atributos_modelos(modelo):
    """ OBTENER ATRIBUTOS DE UN MODELO.

    Retorna todos los atributos de un modelo enviado por parámetro.

    """
    nombres_campos_modelos = [nombre for nombre,_ in mode.fields_for_model(modelo).items()]
    return nombres_campos_modelos

def obtener_modelo(_app_name, _model_name):
    """ OBTENER MODEL.

    Retorna el modelo en cuestión que pertenece a las etiquetas enviadas por parámetros.

    Parámetros:
    -- _app_name                : Nombre de aplicación donde se encuentra el modelo.
    -- _model_name              : Cadena de texto con el nombre de modelo a buscar.

    """
    return apps.get_model(app_label = _app_name, model_name = _model_name)

def obtener_valor_de_atributos_de_modelo(modelo):
    """ OBTENER VALORES PERTENECIENTES A ATRIBUTOS DE UN MODELO.

    Retorna todos los valores que le pertenecen a un modelo en cuestión.

    """
    usuarios = modelo.objects.all().values()
    return [valor for valor in usuarios]

def convertir_booleanos(data):
    """ VALIDACIÓN DE CAMPOS BOOLEANOS ENVIADOS VÍA AJAX.

    Retorna todos los valores enviados vía AJAX convirtiendo a Booleanos los que correspondan.

    """
    """
    temp_data = {}
    claves_temp = []
    valores_temp = []
    for key,value in data.items():
        if '[]' in key:
            key = key.strip('[]')
        if value == "true":
            valores_temp.append(True)
        if value == "false":
            valores_temp.append(False)
        claves_temp.append(key)
        valores_temp.append(value)
    #print(valores_temp)
    data = dict(zip(claves_temp,valores_temp))
    """
    for dat in data:
        if data[dat] == "true":
            data[dat] = True
        if data[dat] == "false":
            data[dat] = False
    return data
