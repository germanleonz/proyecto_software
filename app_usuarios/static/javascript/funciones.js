/*funcion para mostrar dialog*/
function dialog(){
  $("#crearPizarra").click(function(){
    $("#formPizarra").dialog({
      modal:true,
    position: { my: "center", at: "top", of: window },
    dialogClass: 'style_Dialog',
    title: "Registrar Pizarra",
    buttons: {
      "Crear Pizarra": function(){
        valido = validarPizarra();
        if (valido){
          $("#pizarraForm").submit();
          $(this).dialog("close");
        }
      },
    Cancelar: function(){
      $(this).dialog("close");
    }
    }
    });
  });
  $("#crearUsuario").click(function(){
    $("#formUsuario").dialog({
      modal:true,
      position: { my: "center", at: "top", of: window },
      dialogClass: 'style_Dialog',
      title: "Registrar Nuevo Usuario",
      buttons: {
        "Crear un nuevo usuario": function() {
          bValid = validarUsuario();
          if (bValid) {
            // Agregar el usuario recien creado a la lista de usuarios
            $("#usuarioForm").submit();
            $(this).dialog("close");
          } 
        },
      Cancel: function() {
        $(this).dialog("close");
      }
      }
    })
  });

}

/*funcion para mostrar opciones cuando se le da click al nombre de usuario*/
function barraUsuario(){
  $("#nombre").click(function(){
    $("#opcionesUsuario").show();
  });
  $(document).keyup(function(event) {
    if(event.which === 27) {
      $('#opcionesUsuario').hide();
    }
  });
  $(document).mouseup(function (e)
      {
        var container = $("#opcionesUsuario");
        if (container.has(e.target).length === 0)
  {
    container.hide();
  }
      });
}

/*Funcion para ejecutar ajax con django*/
function my_js_callback(data){
  document.getElementById("formPizarra").innerHTML = data.vista;
}

