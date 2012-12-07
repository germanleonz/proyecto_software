/*Chequeo de largo de inputs*/
function checkLength(obj, name, min, max, div){
  var valido = true;
  if (obj.val().length == 0) {
    $(div).html("*" + name + " es requerido");
    return false;
  }
  else if (obj.val().length<min){
    valido = false;
  }
  else if (obj.val().length>max){
    valido = false;
  }

  if (!valido){
    if (min<max){
      $(div).html("*"+name+" debe tener entre "+min+" y "+max+" caracteres");
    }
    else if (min==max){
      $(div).html("*"+name+" debe tener "+max+" caracteres");
    }
  }

  return valido;
}

function chequearNomApe(obj, name, min, max, div){
  var valido = true;
  if (obj.val().length<min){
    valido = false;
  }
  else if (obj.val().length>max){
    valido = false;
  }

  if (!valido){
    if (min<max){
      $(div).html("*"+name+" debe tener entre "+min+" y "+max+" caracteres");
    }
    else if (min==max){
      $(div).html("*"+name+" debe tener "+max+" caracteres");
    }
  }

  return valido;
}

/*Chequeo de regex en inputs*/
function checkRegex(obj, name, regex, div){
  if (!regex.test(obj.val())){
    $(div).html("*"+name+" no es valido");
    return false;
  }
  return true;
}

/*chequear formato de fecha*/
function isDate(obj,div) {
  var valido = true;
  var fecha = obj.val(), dia, mes, anio;
  if (fecha.length !== 10) { 
      print ("error longitud");
    valido = false;
  } 
  // third and sixth character should be '/' 
  if (fecha.substring(2, 3) !== '/' || fecha.substring(5, 6) !== '/') { 
    valido = false;
  } 

  dia = parseInt(fecha.substring(0,2));
  mes = parseInt(fecha.substring(3,5));
  anio = parseInt(fecha.substring(6,10));
  if (dia<1 || dia>31){
    valido = false;
  }
  if (mes<1 || mes>12){
    valido = false;
  }

  if (!valido){
    $(div).html("*El formato de fecha debe ser dd/mm/yyyy");
  }
  return valido;
}

/*Obtener fecha de hoy en string con el formato dd/mm/yyyy*/
function obtenerFechaActual(){
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth()+1; //Enero es 0!
  var yyyy = today.getFullYear();
  if(dd<10){
    dd='0'+dd
  } 
  if(mm<10){
    mm='0'+mm
  } 
  today = dd+'/'+mm+'/'+yyyy;
  return today;
}

/*Compara dos fechas date1>date2 retorna -1, date1<date2 retorna 1 y date1=date2 retorna 0*/
function compareDates(date1, date2){
  dia1 = parseInt(date1.substring(0,2));
  mes1 = parseInt(date1.substring(3,5))-1;
  anio1 = parseInt(date1.substring(6,10));
  fecha1 = new Date(anio1,mes1,dia1);

  if (date2 !== obtenerFechaActual()){
    dia2 = parseInt(date2.substring(0,2));
    mes2 = parseInt(date2.substring(3,5))-1;
    anio2 = parseInt(date2.substring(6,10));
    fecha2 = new Date(anio2,mes2,dia2);

  }
  else{
    fecha2 = new Date();
  }

  if (fecha1 > fecha2){
    return -1;
  }
  else if (fecha1 == fecha2){
    return 0;
  }
  else{
    return 1;
  }
}

function compararContrasenas(contrasena1, contrasena2, div) {
    if ((contrasena1.val()).localeCompare(contrasena2.val()) == 0) {
        return true;
    } else {
        $(div).html("Las contrasenas no coinciden");
    }
    return false;
}


/*funcion para validar el form de crear pizarra*/
function validarPizarra(){
  var nombre = $("#id_nombre"),
      descripcion = $("#id_descripcion"),
      fechaini = $("#id_fecha_inicio"),
      fechafin = $("#id_fecha_final"),
      valido = true,
      formato = /^[A-Za-z0-9\?\¿\!\¡\:\,\.\-\ç\ñáéíóú\(\)\"\'\äëïöüàèìòù\s]*$/,
      div= "#errores_crear_pizarra";

  valido = valido && checkLength(nombre,"Nombre",1,50,div);
  valido = valido && checkLength(descripcion,"Descripcion",1,150,div);
  valido = valido && checkLength(fechaini, "Fecha inicio",10,10,div);
  valido = valido && checkLength(fechafin, "Fecha final",10,10,div);
  valido = valido && checkRegex(nombre,"Nombre",formato,div);
  valido = valido && checkRegex(descripcion,"Descripcion",formato,div);
  valido = valido && isDate(fechaini,div);
  valido = valido && isDate(fechafin,div);

  if (valido && compareDates(fechaini.val(),fechafin.val())==-1){
    valido = false;
    $("#errores_crear_pizarra").html("*La fecha final debe ser mayor a la de inicio");
  }

  today = obtenerFechaActual();

  if (valido && compareDates(fechaini.val(),today)== 1){
    valido = false;
    $("#errores_crear_pizarra").html("*La fecha de inicio debe ser mayor a la de hoy");
  }

  return valido;
}

function validarUsuario(){
  var nombre_usuario = $("#id_nuevo_nombre_usuario"),
      contrasena = $("#id_nueva_password"),
      //contrasena2 = $("#id_nueva_password2"),
      correo = $("#id_nuevo_correo"),
      nombre = $("#id_nuevo_nombre"),
      apellido = $("#id_nuevo_apellido"),
      telefono = $("#id_nuevo_telefono"),
      div = "#errores_crear_usuario",
      formatoNombres = /^[A-Za-z0-9\?\¿\!\¡\:\,\.\-\ç\ñáéíóú\(\)\"\'\äëïöüàèìòù\s]*$/,
      formatoCorreo = /^[a-zA-Z0-9]+[@]?[a-zA-Z]+\.([a-z]{2-4})$/,
      formatoTelefono = /^[0-9]+[-]?[0-9]+$/,
      valido = true;

      valido = valido && checkLength(nombre_usuario,"Nombre de Usuario", 1, 30, div);
      valido = valido && checkLength(contrasena,"Contraseña", 6, 15, div);
      valido = valido && checkLength(correo,"Correo", 1, 30, div);
      valido = valido && checkLength(nombre,"Nombre", 1, 30, div);
      valido = valido && checkLength(apellido,"Apellido", 1, 30, div);
      valido = valido && checkLength(telefono,"Telefono", 1, 30, div);
      //valido = valido && checkRegex(correo,"Correo",formatoCorreo, div);
      valido = valido && checkRegex(nombre,"Nombre",formatoNombres, div);
      valido = valido && checkRegex(telefono,"Telefono",formatoTelefono, div);
      valido = valido && checkRegex(apellido,"Apellido",formatoNombres, div);

      return valido;
}

function validarModificacion(){
  var correo = $("#id_correo"),
      nombre = $("#id_nombre"),
      apellido = $("#id_apellido"),
      telefono = $("#id_telefono"),
      div = "#errores_modificar_usuario",
      formatoNombres = /^[A-Za-z0-9\?\¿\!\¡\:\,\.\-\ç\ñáéíóú\(\)\"\'\äëïöüàèìòù\s]*$/,
      formatoCorreo = /^[a-zA-Z0-9]+[@]?[a-zA-Z]+\.([a-z]{2-4})$/,
      formatoTelefono = /^[0-9]+[-]?[0-9]+$/,
      valido = true;

      valido = valido && checkLength(correo,"Correo", 1, 30, div);
      valido = valido && chequearNomApe(nombre,"Nombre", 0, 30, div);
      valido = valido && chequearNomApe(apellido,"Apellido", 0, 30, div);
      valido = valido && checkLength(telefono,"Telefono", 1, 30, div);
      //valido = valido && checkRegex(correo,"Correo",formatoCorreo, div);
      if (nombre.val().length > 0) { 
          valido = valido && checkRegex(nombre,"Nombre",formatoNombres, div);
      }
      if (apellido.val().length > 0) {
          valido = valido && checkRegex(apellido,"Apellido",formatoNombres, div);
      }
      valido = valido && checkRegex(telefono,"Telefono",formatoTelefono, div);

      return valido;
}

function validarModificarPizarra() {
  var nombre = $("#id_nombre"),
      descripcion = $("#id_descripcion"),
      fechacreacion = $("#id_fecha_creacion"),
      fechafin = $("#id_fecha_final"),
      formato = /^[A-Za-z0-9\?\¿\!\¡\:\,\.\-\ç\ñáéíóú\(\)\"\'\äëïöüàèìòù\s]*$/,
      div = "#errores_modificar_pizarra",
      valido = true;

      valido = valido && checkLength(nombre,"Nombre",1,50,div);
      valido = valido && checkLength(descripcion,"Descripcion",1,150,div);
      valido = valido && checkLength(fechafin, "Fecha final",10,10,div);
    
      if (valido && compareDates(fechacreacion.val(),fechafin.val())==-1){
        valido = false;
        $("#errores_modificar_pizarra").html("*La fecha final debe ser mayor a la de creacion");
      }

      valido = valido && checkRegex(descripcion,"Descripcion",formato,div);

      valido = valido && isDate(fechafin,div);
      return valido;
}

function validarContrasenas() {
    var contrasena1 = $("#id_contrasena1"),
    contrasena2 = $("#id_contrasena2"),
    valido = true,
    div = "#errores_cambiar_contrasena";

    valido = valido && checkLength(contrasena1, "Contrasena", 6, 15, div);
    valido = valido && checkLength(contrasena2, "Repeticion contrasena", 6, 15, div);
    valido = valido && compararContrasenas(contrasena1, contrasena2, div);
    return valido;
}

function validarCorreo() {
    var correo = $("#recipiente"),
    valido = true,
    div = "#errores_asignar_actividad";

    valido = valido && checkLength(correo,"Correo",1,50,div);
    return valido;
}


function validarActividad(){
  var nombre = $("#id_nombre"),
      descripcion = $("#id_descripcion"),
      fechaini = $("#id_fecha_inicio"),
      fechafin = $("#id_fecha_final"),
      valido = true,
      formato = /^[A-Za-z0-9\?\¿\!\¡\:\,\.\-\ç\ñáéíóú\(\)\"\'\äëïöüàèìòù\s]*$/
      div = "#errores_crear_actividad";

  valido = valido && checkLength(nombre,"Nombre",1,50,div);
  valido = valido && checkLength(descripcion,"Descripcion",1,150,div);
  valido = valido && checkLength(fechaini, "Fecha inicio",10,10,div);
  valido = valido && checkLength(fechafin, "Fecha final",10,10,div);
  valido = valido && checkRegex(nombre,"Nombre",formato,div);
  valido = valido && checkRegex(descripcion,"Descripcion",formato,div);
  valido = valido && isDate(fechaini,div);
  valido = valido && isDate(fechafin,div);

  if (valido && compareDates(fechaini.val(),fechafin.val())==-1){
    valido = false;
    $("#errores_crear_pizarra").html("*La fecha final debe ser mayor a la de inicio");
  }

  today = obtenerFechaActual();

  if (valido && compareDates(fechaini.val(),today)== 1){
    valido = false;
    $("#errores_crear_pizarra").html("*La fecha de inicio debe ser mayor a la de hoy");
  }
  return valido;
}
