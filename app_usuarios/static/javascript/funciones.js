/*
 * Este archivo contiene las siguientes funciones:
 * dialog: funcion que crea los dialogs para toda la pagina
 * barraUsuario: funcion que muestra la barra de opciones cuando se le da click al nombre de usuario
 * my_js_callback* : funciones que se llaman con dajaxice para usar ajax con django
 *
 */

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
      Cancel: function() {
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
      Cancel: function() {
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
      Cancel: function() {
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
      Cancel: function() {
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

function my_js_callbackContrasena(data){
  $("#dialogCambiarContrasena").html(data.vista);
}

function dibujarGrafo(Lados){
  window.jsPlumbDemo = {
    init : function() {
      jsPlumb.importDefaults({
      Connector : [ "Bezier", { curviness:50 } ],
      DragOptions : { cursor: "pointer", zIndex:2000 },
      PaintStyle : { strokeStyle:color, lineWidth:2 },
      EndpointStyle : { radius:0, fillStyle:color },
      HoverPaintStyle : {strokeStyle:"#ec9f2e" },
      EndpointHoverStyle : {fillStyle:"#ec9f2e" },
      Anchors :  [ "BottomCenter", "TopCenter" ]
      });
      var arrowCommon = { 
        foldback:0.7, fillStyle:color, width:14},
          overlays = [];

      var i;
      for (i=0; i<Lados.length; ++i){
        jsPlumb.connect({
          source:Lados[i][0], 
          target:Lados[i][1], overlays:overlays, detachable:false, reattach:true});
      }
      jsPlumb.draggable(jsPlumb.getSelector(".window"));

    }
  }
}
