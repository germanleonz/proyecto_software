from django import template
import time

register = template.Library()


@register.filter
def fecha(value):
    """
    Metodo que transforma string en struct_time
    """
    try: 
        return (time.strptime(value,"%b %d, %Y"))
    except AttributeError:
        return ''

@register.filter
def fechaFormateada(value, arg):
    """
    Metodo que cambia el formato de una fecha a arg
    """
    try:
        return time.strftime(arg,value)
    except AttributeError:
        return ''

