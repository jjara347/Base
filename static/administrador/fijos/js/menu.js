function obtenerEmpresaInicial(){
    $.ajax({
        url: '/menu/empresa_inicial/',
        type: 'get',
        dataType: 'json',
        async: false,
        success: function(response){
          let temporal_empresa = '<h3>' + response[0]['ESd_Nombre']+'</h3>';
          $('#empresa').html("");
          $('#empresa').html(temporal_empresa);
          document.title = response[0]['ESd_Nombre'];
          pintarMenu(response[0]['id']);
        }
    });
}

function abrirModalEmpresas(){
  obtenerEmpresas();
  $('#default-Modal').modal('show');
}

function cerrarModalEmpresas(){
  let data = {};
  data['id'] = document.getElementById('empresas').value;
  $.ajax({
      url: '/menu/empresa_inicial/',
      type:'post',
      data: data,
      async: false,
      success: function(response){
        location.href="/administrador/";
        //javascript:location.reload();
        obtenerEmpresaInicial();
      },
      error:function(error){
        console.log(error);
      }
  });
  $('#default-Modal').modal('hide');
}

function obtenerEmpresas(){
    $.ajax({
        url: '/menu/empresas/',
        type: 'get',
        dataType: 'json',
        async: false,
        success: function(response){
          var empresas = [];
          var id_empresas = [];
          $('#empresas').html("");
          var select = document.getElementById("empresas");
          for(item in response){
            empresas.push(response[item]['nombre']);
            id_empresas.push(response[item]['id'])
          }
          for(var i = 0; i < empresas.length; i++){
              var option = document.createElement("option");
              option.innerHTML = empresas[i];
              option.value = id_empresas[i];
              select.appendChild(option);
          }
        }
    });
}

function pintarMenu(empresa_inicial){
    $.ajax({
        url: '/menu/'+empresa_inicial+'/',
        type: 'get',
        async: false,
        success: function(response){
          $('#renderMenu').html("");
          $('#renderMenu').html(response);
        }
    });
}
