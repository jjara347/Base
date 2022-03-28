function activarBoton() {
    if (document.getElementById("botonRegistrar").disabled) {
        document.getElementById("botonRegistrar").disabled = false;
    } else {
        document.getElementById("botonRegistrar").disabled = true;
    }
}
function limpiarFormularioRegistro() {
    $("#id_nombre").val("");
    $("#id_icono").val("");
}

function buscar(id) {
    for (item in temporales) {
        if (temporales[item]["pk"] == id)
            return temporales[item]["fields"]["nombre"];
    }
}

function abrirModalEliminacion(id) {
    let item = buscar(id);
    temporal = id;
    $("#modalEliminacion").modal("show");
    $("#texto_modal_eliminacion").html(
        "<h3>Está a punto de eliminar el item <strong>" +
        item +
        ",</strong><strong>¿Está seguro que desea eliminarlo?</strong></h3>"
    );
}

function abrirModalEdicion(id) {
    let url = "/menu/mantenimiento/actualizar_item/" + id + "/";
    temporal = id;
    $("#modalEdicion").load(url, function () {
        $(this).modal("show");
    });
}
function noti(mensaje) {
    notificacionSuccess(mensaje);
}

/*
  
        ******************* PETICIONES AJAX ************************
  
  */

function registrarItem() {
    activarBoton();
    $.ajax({
        data: $("#form-creacion").serialize(),
        url: "/menu/item/crear/",
        type: $("#form-creacion").attr("method"),
        dataType: "json",
        success: function (response) {
            limpiarFormularioRegistro();
            activarBoton();
            listarItemRegistrados();
            //noti(response.mensaje);
        },
        error: function (response) {
            console.log(response);
            activarBoton();
            $("#errores").html("");
            let error = "";
            for (let item in response.responseJSON.error) {
                console.log(response.responseJSON.error[item]);
                error +=
                    '<div class="alert alert-danger"><strong>' +
                    response.responseJSON.error[item] +
                    "</strong></div>";
            }
            $("#errores").append(error);
            setTimeout(function () {
                $("#errores").html("");
            }, 2000);
        }
    });
}

function listarItemRegistrados() {
    $.ajax({
        url: "/menu/item/",
        dataType: "json",
        type: "get",
        async: false,
        success: function (response) {
            $("#tabla tbody").html("");
            temporales = response;
            for (let index = 0; index < response.length; index++) {
                let fila = "<tr>";
                fila +=
                    '<td class = "text-center">' +
                    response[index]["fields"]["nombre"] +
                    "</td>";
                fila +=
                    '<td class = "text-center">' +
                    response[index]["fields"]["url"] +
                    "</td>";
                fila +=
                    '<td class = "text-center">' +
                    response[index]["fields"]["icono"] +
                    "</td>";
                let grupo_permisos = "";
                for (em in response[index]["fields"]["grupo_permisos"]) {
                    grupo_permisos +=
                        response[index]["fields"]["grupo_permisos"][em] + " ";
                }
                fila += '<td class = "text-center">' + grupo_permisos + "</td >";
                if (response[index]["fields"]["estado"] == false) {
                    fila += '<td class = "text-center"> Desactivada </td>';
                } else {
                    fila += '<td class = "text-center"> Activada </td>';
                }
                fila +=
                    '<td class = "text-center">' +
                    response[index]["fields"]["fecha_creacion"] +
                    "</td>";
                fila +=
                    '<td class = "text-center"><button  class = "btn btn-primary separacion_botones btn-outline-info waves-effect md-trigger" onclick = "abrirModalEdicion(' +
                    response[index]["pk"] +
                    ');">Editar</button>';
                fila +=
                    '<button onclick = "abrirModalEliminacion(' +
                    response[index]["pk"] +
                    ')" class = "btn btn-danger separacion_botones"';
                fila += ">Eliminar</button></td>";
                fila += "</tr>";
                $("#tabla tbody").append(fila);
            }
            $("#tabla").DataTable();
        }
    });
}

function eliminarItem() {
    $.ajax({
        url: "/menu/item/" + temporal + "/eliminar/",
        type: "post",
        success: function (response) {
            //noti(response.mensaje);
            listarItemRegistrados();
        },
        error: function (response) {
            $("#errores").html("");
            let error = "";
            for (let item in response.responseJSON.error) {
                console.log(response.responseJSON.error[item]);
                error +=
                    '<div class="alert alert-danger"><strong>' +
                    response.responseJSON.error[item] +
                    "</strong></div>";
            }
            $("#errores").append(error);
            setTimeout(function () {
                $("#errores").html("");
            }, 2000);
        }
    });
}

$(document).ready(function () {
    var temporal;
    var temporales;
    listarItemRegistrados();
});
