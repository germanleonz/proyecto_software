from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
import re


"""
Form para crear nueva pizarra
"""
class CrearActividadForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    descripcion = forms.CharField(max_length=100, widget=forms.Textarea)
    fecha_inicio = forms.DateField()
    fecha_final = forms.DateField()

class ModificarActividadForm(forms.Form):
    nombreact = forms.CharField(max_length=50)
    descripcionact = forms.CharField(max_length=100)
    fechainicial = forms.DateField()
    fechaentrega = forms.DateField()
    
class CambiarEstadoForm(forms.Form):
    estadoact = forms.CharField(max_length=15)
