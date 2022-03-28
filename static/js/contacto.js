function limpiarFormulario(){
  $('#id_apellidos').val("");
  $('#id_nombres').val("");
  $('#id_correo').val("");
  $('#id_asunto').val("");
  $('#id_mensaje').val("");
}


function registrarContacto(){
    let data = {}
    data['apellidos'] = $('#id_apellidos').val();
    data['nombres'] = $('#id_nombres').val();
    data['correo'] = $('#id_correo').val();
    data['asunto'] = $('#id_asunto').val();
    data['mensaje'] = $('#id_mensaje').val();
    $.ajax({
        data: data,
        url: '/contacto/formulario_contacto/',
        type: 'post',
        success: function(response){
            $('#mensajes').html("");
            let mensaje = '<h2 style = "color:green;">'+response['mensaje']+'</h2>';
            $('#mensajes').html(mensaje);
            limpiarFormulario();
            setTimeout(function(){
                $('#mensajes').html("");
              },2000);
        },
        error: function(response){
          $('#mensajes').html("");
          let mensaje = '<h2 style = "color:red;">'+response['error']+'</h2>';
          $('#mensajes').html(mensaje);
          setTimeout(function(){
              $('#mensajes').html("");
            },2000);
        }
    });
}
