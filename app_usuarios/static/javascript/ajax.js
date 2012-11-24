function AJAXRequest(url,div){
  var xmlhttp;
  alert("hola");

  if (window.XMLHttpRequest){
    xmlhttp = new XMLHttpRequest();
  }
  else{
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }

  xmlhttp.open("POST",url, true);
  xmlhttp.send(); 
  xmlhttp.onreadystatechange = function(){
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
      document.getElementById(id).innerHTML=xmlhttp.responseText;
    }
  }   
}
