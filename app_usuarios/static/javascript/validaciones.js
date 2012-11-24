function checkLength(min, max, value){
  if (value.val().length > max || value.val().length <min)
    return false;
  
  return true;
}

function checkEmail(value, regexp){
  if (!( regexp.test(value.val()))){
    return false;
  }
  return true;
}
