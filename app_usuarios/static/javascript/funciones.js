/*
 * Este archivo contiene las siguientes funciones:
 * dialog: funcion que crea los dialogs para toda la pagina
 * barraUsuario: funcion que muestra la barra de opciones cuando se le da click al nombre de usuario
 * my_js_callback* : funciones que se llaman con dajaxice para usar ajax con django
 *
 */
/*Funcion para crear los calendarios*/
function calendarios(){
    //calendarios fecha de inicio
    $("#id_fecha_inicio").datepicker({
        changeMonth: true,
        changeYear: true
    });
    $( "#id_fecha_inicio" ).datepicker(
      "option", "dateFormat", "dd/mm/yy" 
    );

    $( "#id_fecha_inicio" ).datepicker({
        dayNamesMin: [ "Dom", "Lun", "Mar", "Mie", "Juev", "Vier", "Sab" ] 
    });   

    var dayNamesMin = $( "#id_fecha_inicio" ).datepicker( "option", "dayNames" );
    $( "#id_fecha_inicio" ).datepicker( 
      "option", "dayNamesMin", [ "Dom", "Lun", "Mar", "Mie", "Juev", "Vier", "Sab" ] 
    );

    $( "#id_fecha_inicio" ).datepicker( "option", "yearRange", "1970:2012" );

    //calendarios fecha de entrega
    $("#id_fecha_final").datepicker({
        changeMonth: true,
        changeYear: true
    });

    $( "#id_fecha_final" ).datepicker(
      "option", "dateFormat", "dd/mm/yy" 
    );

    $( "#id_fecha_final" ).datepicker({
        dayNamesMin: [ "Dom", "Lun", "Mar", "Mie", "Juev", "Vier", "Sab" ] 
    });   

    var dayNamesMin = $( "#id_fecha_final" ).datepicker( "option", "dayNames" );
    $( "#id_fecha_final" ).datepicker( 
      "option", "dayNamesMin", [ "Dom", "Lun", "Mar", "Mie", "Juev", "Vier", "Sab" ] 
    );

    $( "#id_fecha_final" ).datepicker( "option", "yearRange", "1970:2012" );
};

/*funcion para mostrar dialog*/
function dialog(){
  /*dialog de crear pizarra*/
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

  /*dialog de modificar pizarra*/
  $(".modi").click(function(){
    $("#dialogModificarPizarra").dialog({
      modal:true,
    position: { my: "center", at: "top", of: window },
    dialogClass: 'style_Dialog',
    title: "Modificar Pizarra",
    buttons: {
      "Modificar": function(){
        valido = validarModificarPizarra();
        if (valido){
          $("#modificarPizarraForm").submit();
          $(this).dialog("close");
        }
      },
    Cancelar: function(){
      $(this).dialog("close");
    }
    }
    });
  });

  /*dialog de crear usuario*/
  $("#crearUsuario").click(function(){
    $("#dialogCrearUsuario").dialog({
      modal:true,
      position: { my: "center", at: "top", of: window },
      dialogClass: 'style_Dialog',
      title: "Registrar Nuevo Usuario",
      buttons: {
        "Crear un nuevo usuario": function() {
          bValid = validarUsuario();
          if (bValid) {
            // Agregar el usuario recien creado a la lista de usuarios
            $("#crearUsuarioForm").submit();
            $(this).dialog("close");
          } 
        },
      Cancelar: function() {
        $(this).dialog("close");
      }
      }
    })
  });

  /*dialog de modificar usuario*/
  $(".modificarUsuario").click(function() {
    $("#dialogModificarUsuario").dialog({
      modal:true,
      position: { my: "center", at: "top", of: window },
      dialogClass: 'style_Dialog',
      title: "Modificar usuario",
      buttons: {
        "Modificar usuario": function() {
          bValid = validarModificacion();
          if (bValid) {
            // Agregar el usuario recien creado a la lista de usuarios
            $("#modificarUsuarioForm").submit();
            $(this).dialog("close");
          } 
        },
      Cancelar: function() {
        $(this).dialog("close");
      }
      }
    })
  });

  /*dialog de editar perfil*/
  $("#editarPerfil").click(function() {
    $("#dialogEditarPerfil").dialog({
      modal:true,
      position: { my: "center", at: "top", of: window },
      dialogClass: 'style_Dialog',
      title: "Editar Perfil",
      buttons: {
        "Editar perfil": function() {
          bValid = validarModificacion();
          if (bValid) {
            // Agregar el usuario recien creado a la lista de usuarios
            $("#modificarUsuarioForm").submit();
            $(this).dialog("close");
          } 
        },
      Cancelar: function() {
        $(this).dialog("close");
      }
      }
    })
  });

  /*dialog de cambiar contrasena*/
  $("#cambiarContrasena").click(function() {
    $("#dialogCambiarContrasena").dialog({
      modal:true,
      position: { my: "center", at: "top", of: window },
      dialogClass: 'style_Dialog',
      title: "Cambiar contrasena",
      buttons: {
        "Cambiar contrasena": function() {
          bValid = validarContrasenas();
          if (bValid) {
            // Cambiar contrasena del usuario
            $("#cambiarContrasenaForm").submit();
            $(this).dialog("close");
          } 
        },
      Cancelar: function() {
        $(this).dialog("close");
      }
      }
    })
  });

  /*dialog de crearActividad*/
  $("#crearActividad").click(function(){
    $("#formActividad").dialog({
      modal:true,
      position: { my: "center", at: "top", of: window },
      dialogClass: 'style_Dialog',
      title: "Nueva Actividad",
      buttons: {
        "Crear Actividad": function(){
          valido = validarActividad();
          if (valido){
            $("#actividadForm").submit();
            $(this).dialog("close");
          }

        },
        Cancelar: function(){
          $(this).dialog("close");
        }
      }
    })
    });

  /*dialog de asignarActividad*/
  $("#asignarActividad").click(function(){
    $("#dialogAsignarActividad").dialog({
      modal:true,
      position: { my: "center", at: "top", of: window },
      dialogClass: 'style_Dialog',
      title: "Asignar Actividad",
      buttons: {
        "Asignar Actividad": function(){
          valido = validarCorreo();
          if (valido){
            $("#asignarActividadForm").submit();
            $(this).dialog("close");
          }

        },
        Cancelar: function(){
          $(this).dialog("close");
        }
      }
    })
    });

  /*dialog de modificarActividad*/
  $("#modificarActividad").click(function(){
    $("#formActividad").dialog({
      modal:true,
      position: { my: "center", at: "top", of: window },
      dialogClass: 'style_Dialog',
      title: "Modificar Actividad",
      buttons: {
        "Modificar Actividad": function(){
          valido = validarActividad();
          if (valido){
            $("#actividadForm").submit();
            $(this).dialog("close");
          }

        },
        Cancelar: function(){
          $(this).dialog("close");
        }
      }
    })
    });


  /*dialog de ver actividad
  $(".mostrarActividad").click(function(){
    $("#ventanaActividad").dialog({
      modal:true,
      width: 800,
      position: { my: "center", at: "top", of: window },
      dialogClass: 'style_Dialog',
      title: 'Actividad',
    })
  })*/


}

/*funcion para mostrar opciones cuando se le da click al nombre de usuario*/
function barraUsuario(){
  /*Para mostrar y esconder la barra clickeando en el nombre*/
  $("#nombre").click(function(){
    $("#opcionesUsuario").toggle();
      })
  /*Para esconder con ESC*/
  $(document).keyup(function(event) {
    if(event.which === 27) {
      $('#opcionesUsuario').hide();
    }
  });
  /*Para esconder con click afuera */
  $(document).click(function(e){
      if (!(e.target.id == "opcionesUsuario") && !(e.target.id == "nombre")){
        $('#opcionesUsuario').hide();
      }
    })
}

/*Funciones para ejecutar ajax con django*/
function my_js_callbackPizarra(data){
  $("#formPizarra").html(data.vista);
}

function my_js_callbackModificarPizarra(data){
  $("#dialogModificarPizarra").html(data.vista);
}

function my_js_callbackUsuario(data) {
  $("#dialogCrearUsuario").html(data.vista);
};

function my_js_callbackModificarUsuario(data) {
  $("#dialogModificarUsuario").html(data.vista);
};

function my_js_callbackPerfil(data) {
  $("#dialogEditarPerfil").html(data.vista);
};

function my_js_callbackActividad(data){
  $("#formActividad").html(data.vista);
}

function visualizarActividad(data){
  $("#ventanaActividad").html(data.vista);
}

function my_js_callbackAsignarActividad(data) {
  $("#dialogAsignarActividad").html(data.vista);
}

function my_js_callbackModificarActividad(data){
  $("#dialogModificarActividad").html(data.vista);
}
function my_js_callbackContrasena(data){
  $("#dialogCambiarContrasena").html(data.vista);
}
