from django import forms
from django.core.exceptions import ValidationError
import re

def validate_nombrepiz(value):
    if re.match('^[a-zA-Z]+$',value)==None:
        raise ValidationError(u'\"%s\" no es un nombre valido' % value)

def validate_descripcionpiz(value):
    if re.match('^\w+$',value)==None:
        raise ValidationError(u'agregue una descripcion')



class CrearPizarraForm(forms.Form):
    """
    Form para crea pizarra
    """
    nombre = forms.CharField(max_length=50)
    descripcion = forms.CharField(max_length=100, widget=forms.Textarea)
    fecha_inicio = forms.DateField()
    fecha_final = forms.DateField()

class ModificarPizarraForm(forms.Form):
    """
    Form para modificar pizarra
    """
    input_formats = ('%d/%m/%Y',)
    nombre = forms.CharField(max_length=50)
    descripcion = forms.CharField(max_length=100, widget=forms.Textarea)
    fecha_final = forms.DateField(input_formats=input_formats)

