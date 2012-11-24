from django import forms
from django.core.exceptions import ValidationError

#def validate_contenidoNoNulo(value):
#    if re.match('^\w+$',value)==None:
#        raise ValidationError(u'agregue un comentario')

"""
Form para hacer un comentario
"""
class CrearComentarioForm(forms.Form):
#  idactividad = forms.IntegerField()
  contenido = forms.CharField(max_length=200)
