function registrarUsuario(){
  /* PETICIÓN AJAX PARA REGISTRO DE UN USUARIO EN LA BASE DE DATOS.

    Realiza una petición AJAX para el registro de un nuevo usuario en la base de datos,
    el primer paso es desactivar el botón de registro para evitar enviós múltiples de la petición,
    luego se captura cada uno de los valores del formulario de registro a traves de sus id para
    guardarlos en un diccionario llamado "data".
    Este diccionario será el enviado en la petición AJAX a la url correspondiente, al ser enviada
    la petición pueden suceder 2 casos:

              **SUCCESS:
                  Si la petición obtuvo una respuesta correcta por parte del backend, se procede a
                  ejecutar una lista de funciones, las cuales son:

                      - limpiarFormularioRegistroUsuario() -- limpia los campos del formulario de registro.
                      - activarBoton() -- activa el botón de registro.
                      - listarUsuariosRegistrados() -- refresca la tabla con que contiene los usuarios registrdos.
                      - noti() -- muestra la notificación con el mensaje de éxito en la creación.


              **ERROR:
                  Si la petición obtuvo una respuesta errónea por parte del backend, se procede a pintar
                  la lista de errores que no permitió que la petición fuera aceptada.

  */
    let data = {}
    data['apellidos'] = $('#apellidos').val();
    data['nombres'] = $('#nombres').val();
    data['mayor'] = $('#mayor').val();
    $.ajax({
        data: data,
        url: '/new/hombre/',
        type: 'post',
        success: function(response){
        },
        error: function(response){
        }
    });
}
function abrirModalEdicion(id){
  //let url = '/persona/'+id+'/update';
  let url = '/base/actualizar/'+id+'/';
  usuario_temporal = id;
  $('#modalEdicion').load(url,function(){
      $(this).modal('show');
    });
}
function listarPersonasRegistradas(){
/* PETICIÓN AJAX QUE PINTA LA LISTA DE USUARIOS REGISTRADOS Y ACTIVADOS EN LA BASE DE DATOS.

  Se envía una petición AJAX al backend solicitando la lista de usuarios que estén registrados en la
  base de datos y que estén activados.
  Se utiliza un --DataTable-- para el renderizado de los usuarios, se le agrega una configuración de
  idioma, así como una validación de destrucción de una posible existencia de la misma para no
  obtener un error de renderizado.

  Variables:
  parametros -- aquí se guarda el valor que se escriba en la barra de búsqueda del DataTable para ser
                enviado en la petición AJAX por si se desee realizar algpun filtro.

*/
    if ( $.fn.dataTable.isDataTable( '#data-table-basic' ) ) {
        var table = $('#data-table-basic').DataTable();
        table.destroy();
    }
    $('#data-table-basic').DataTable({
        responsive: true
    });
    let parametros = {
        "i" : $("#search").val()
    };
    $.ajax({
        data: parametros,
        url: '/persona/',
        dataType: 'json',
        type: 'get',
        success: function(response){
            $('#data-table-basic').html("");
            usuarios_temporales = response;
            let id_temporal;
            for (let index = 0; index < response.length; index++){
                let fila = '<tr>';
                for(let item in response[index]){
                  if(item == 'pk'){
                    id_temporal = response[index][item];
                  }
                  if(item == 'fields'){

                    fila += '<td class = "text-center">'+response[index][item]['nombres']+'</td>';
                    fila += '<td class = "text-center">'+response[index][item]['apellidos']+'</td>';
                    fila += '<td class = "text-center"><button  class = "btn btn-primary separacion_botones" onclick = "abrirModalEdicion('+id_temporal+');">Editar</button>';
                    fila += '<button onclick = "eliminarPersona('+id_temporal+')" class = "btn btn-danger separacion_botones"';
                    fila += '>Eliminar</button></td>';
                    fila += '</tr>';

                  }
                }
                $('#data-table-basic').append(fila);
            }
            $("#data-table-basic").DataTable({
                destroy: true,
                "language": {
                    "url": "https://cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
                },
                "search": {
                    "caseInsensitive": false
                }
            } );
        }

    });
}

function eliminarPersona(id){
  $.ajax({
      url: '/persona/'+id+'/delete',
      type: 'post',
      success: function(response){
          console.log(response);
          listarPersonasRegistradas();
      },
      error: function(response){
      }
  });
}


$(document).ready(function (){
  var usuario_temporal;
  var usuarios_temporales;
  listarPersonasRegistradas();
});
