function limpiarSuscripcion(){
  $('#correo').val("");
}


function registrarSuscripcion(){
    let data = {}
    data['correo'] = $('#correo').val();
    $.ajax({
        data: data,
        url: '/suscripcion/suscribir/',
        type: 'post',
        success: function(response){
            $('#mensajes').html("");
            let mensaje = '<h2 style = "color:green;">'+response['mensaje']+'</h2>';
            $('#mensajes').html(mensaje);
            limpiarSuscripcion();
            setTimeout(function(){
                $('#mensajes').html("");
              },2000);
        },
        error: function(response){
          $('#mensajes').html("");
          let mensaje = '';
          for (item in response.responseJSON['error']) {
            mensaje += '<h4 style = "color:red;">'+response.responseJSON['error'][item]+'</h4>';
          }
          $('#mensajes').html(mensaje);
          setTimeout(function(){
              $('#mensajes').html("");
            },2000);
        }
    });
}
