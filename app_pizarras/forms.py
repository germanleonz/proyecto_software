from django import forms
from django.core.exceptions import ValidationError
import re

def validate_nombrepiz(value):
    """
    Metodo que valida el formato del nombre de la pizarra. Expresion regular: '^[a-zA-Z]+$
    In: value
    Out: --
    Autor: Mary Ontiveros
    Fecha: 7-11-12
    """
    if re.match('^[a-zA-Z]+$',value)==None:
        raise ValidationError(u'\"%s\" no es un nombre valido' % value)

def validate_descripcionpiz(value):
    """
    Metodo que valida el formato de la descripcion de la pizarra. Expresion regular: '^[a-zA-Z]+$
    In: value
    Out: --
    Autor: Mary Ontiveros
    Fecha: 7-11-12
    """
    if re.match('^\w+$',value)==None:
        raise ValidationError(u'agregue una descripcion')

class CrearPizarraForm(forms.Form):
    """
    Form para crea pizarra
    In: forms.Form
    Out: --
    Autor: Juan Arocha
    Fecha: 7-11-12 Version 1.0
    """
    nombre = forms.CharField(max_length=50)
    descripcion = forms.CharField(max_length=100, widget=forms.Textarea)
    fecha_inicio = forms.DateField()
    fecha_final = forms.DateField()

class ModificarPizarraForm(forms.Form):
    """
    Form para modificar pizarra
    In: forms.Form
    Out: --
    Autor: Juan Arocha
    Fecha: 7-11-12 Version 1.0
    """
    input_formats = ('%d/%m/%Y',)
    nombre = forms.CharField(max_length=50)
    descripcion = forms.CharField(max_length=100, widget=forms.Textarea)
    fecha_final = forms.DateField(input_formats=input_formats)

