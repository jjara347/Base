/*

    ******************** FUNCIONES SIMPLES *******************************
              Aquellas que solo son para activar o desactivar un botón,
              abrir un modal, abrir ventana de notificación, limpiar un
              formulario, etc.

*/

function activarBoton() {
  /* ACTIVAR O DESACTIVAR BOTÓN REGISTRAR USUARIO.

    Activa o desactiva el botón de creación de un usuario, el cual está en el formulario
    de creación. Esto se realiza debido a que pueden existir falsos toques y la petición
    se envíe más de una vez.
    La activación o desactivación se hace a través del id del botón.

  */
  if (document.getElementById("botonRegistrar").disabled) {
    document.getElementById("botonRegistrar").disabled = false;
  } else {
    document.getElementById("botonRegistrar").disabled = true;
  }
}

function limpiarFormularioRegistroUsuario() {
  /* LIMPIAR CAMPOS DE FORMULARIO DE REGISTRO DE USUARIO.

    Limpia cada uno de los campos que tiene el formulario de registro de un nuevo usuario.
    Este proceso se realiza mediante el id que tiene asignado cada uno de los campos HTML.

  */
  $("#UmUsr_Username").val("");
  $("#UmUsr_Apellidos").val("");
  $("#UmUsr_Nombres").val("");
  $("#password1").val("");
  $("#password2").val("");
  $("#UmUsr_Email").val("");
}

function buscarUsuario(id) {
  /* BUSCAR EL USERNAME DE UN USUARIO REGISTRADO EN LA BASE DE DATOS.

    Esta función recorre la variable tempotal usuarios_temporales, la cuál contiene los usuarios
    existentes y que se encuentran en la tabla de muestra, busca en ellos un usuario específico
    y retorna su nombre de usuario (username)

    Parámetros:
    id -- clave primaria del usuario a buscar.

    Variables:
    usuarios_temporales -- lista con los usuarios activos y registrados en la base de datos que se
                           muestran en la tabla de listado de usuarios.

  */
  for (item in usuarios_temporales) {
    if (usuarios_temporales[item]["id"] == id)
    return usuarios_temporales[item]["username"];
  }
}

function abrirModalEliminacion(id) {
  /* ABRIR MODAL DE CONFIRMACIÓN DE ELIMINACIÓN DE USUARIO.

    Abre el modal de confirmación de la eliminación de un usuario.Además coloca el mensaje de
    eliminación en el modal con el nombre del usuario seleccionado, asi mismo guarda en la
    variable temporal usuario_temporal el id con el usuario que se está deseando eliminar.

    Parámetros:
    id -- clave primaria del usuario a buscar.
    usuario_temporal -- variable global que guarda el id del usuario que se desea eliminar o editar.

  */
  let usuario = buscarUsuario(id);
  console.log(usuario);
  usuario_temporal = id;
  $("#modalEliminacion").modal("show");
  $("#texto_modal_eliminacion").html(
    "<h3>Está a punto de eliminar al usuario <strong>" +
    usuario +
      ",</strong><strong>¿Está seguro que desea eliminarlo?</strong></h3>"
  );
}

function abrirModalEdicion(id) {
  let url = "/usuarios/actualizar_usuario/" + id + "/";
  usuario_temporal = id;
  $("#modalEdicion").load(url, function() {
    $(this).modal("show");
  });
}

//function noti(mensaje){
/* NOTIFICAICÓN POP UP.

    Abre un pop up de notificación mostrando un mensaje asegurando que la eliminación se realizó correctamente.

    Parámetros:
    mensaje -- mensaje que se desea mostrar en la notificación pop up, el cuál se obtiene desde la base de datos.

    Funciones:
    notificacionSuccess() -- función JS que muestra la notificación pop up con el mensaje enviado.
  */
//notificacionSuccess(mensaje);
//}

/*

      ******************* PETICIONES AJAX ************************

*/

function registrarUsuario() {
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
  activarBoton();
  $.ajax({
    data: $("#form-creacion").serialize(),
    url: "/usuarios/usuarios/usuario/",
    type: $("#form-creacion").attr("method"),
    dataType: "json",
    success: function(response) {
      limpiarFormularioRegistroUsuario();
      activarBoton();
      listarUsuariosRegistrados();
      //noti(response.mensaje);
    },
    error: function(response) {
      activarBoton();
      $("#errores").html("");
      let error = "";
      for (let item in response.responseJSON.mensaje) {
        for (let i in response.responseJSON.mensaje[item]) {
          console.log(response.responseJSON.mensaje[item]);
          error +=
            '<div class="alert alert-danger"><strong>' +
            response.responseJSON.mensaje[item][i] +
            "</strong></div>";
        }
      }
      $("#errores").append(error);
      setTimeout(function() {
        $("#errores").html("");
      }, 2000);
    }
  });
}

function listarUsuariosRegistrados() {
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
  $.ajax({
    url: "/usuarios/usuarios/usuario/",
    dataType: "json",
    type: "get",
    async: false,
    success: function(response) {
      $("#tabla tbody").html("");
      usuarios_temporales = response;
      for (let index = 0; index < response.length; index++) {
        let fila = "<tr>";
        // EJEMPLO DE UNA FILA
        fila +=
          '<td class = "text-center">' + response[index]["username"] + "</td>";
        fila +=
          '<td class = "text-center">' + response[index]["nombres"] + "</td>";
        fila +=
          '<td class = "text-center">' + response[index]["apellidos"] + "</td>";
        fila +=
          '<td class = "text-center">' + response[index]["email"] + "</td>";
        if (response[index]["usuario_administrador"] == false) {
          fila += '<td class = "text-center"> No </td>';
        } else {
          fila += '<td class = "text-center"> Si </td>';
        }
        fila +=
          '<td class = "text-center"><button  class = "btn btn-primary separacion_botones" onclick = "abrirModalEdicion(' +
          response[index]["id"] +
          ');">Editar</button>';
        fila +=
          '<button onclick = "abrirModalEliminacion(' +
          response[index]["id"] +
          ')" class = "btn btn-danger separacion_botones"';
        fila += ">Eliminar</button></td>";
        fila += "</tr>";
        $("#tabla tbody").append(fila);
      }
      $("#tabla").DataTable();
    }
  });
}

function eliminarUsuario() {
  /* PETICIÓN AJAX PARA ELIMINACIÓN LÓGICA DE UN USUARIO REGISTRADO EN LA BASE DE DATOS.

    Realiza una petición AJAX para la eliminación lógica de un usuario registrado en la base de datos,
    para lo cuál se utiliza la variable global usuario_temporal que guarda el --id-- del usuario a eliminar,
    este --id-- se envía a la URL para que se pueda validar en el backend.
    Al enviar la petición se puede dar cualquiera de los siguientes casos:

              **SUCCESS:
                  Si la petición obtuvo una respuesta correcta por parte del backend, se procede a
                  ejecutar una lista de funciones, las cuales son:

                      - listarUsuariosRegistrados() -- refresca la tabla con que contiene los usuarios registrdos.
                      - noti() -- muestra la notificación con el mensaje de éxito en la creación.


              **ERROR:
                  Si la petición obtuvo una respuesta errónea por parte del backend, se procede a pintar
                  la lista de errores que no permitió que la petición fuera aceptada.

  */
  $.ajax({
    url: "/usuarios/eliminar_usuario/" + usuario_temporal + "/",
    type: "post",
    success: function(response) {
      //noti(response.mensaje);
      listarUsuariosRegistrados();
    },
    error: function(response) {
      $("#errores").html("");
      let error = "";
      for (let item in response.responseJSON.mensaje) {
        for (let i in response.responseJSON.mensaje[item]) {
          error +=
            '<div class="alert alert-danger"><strong>' +
            response.responseJSON.mensaje[item][i] +
            "</strong></div>";
        }
      }
      $("#errores").append(error);
      setTimeout(function() {
        $("#errores").html("");
      }, 2000);
    }
  });
}

$(document).ready(function() {
  var usuario_temporal;
  var usuarios_temporales;
  listarUsuariosRegistrados();
});
