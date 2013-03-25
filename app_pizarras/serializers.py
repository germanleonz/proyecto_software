from rest_framework import serializers
from app_pizarras.models import Pizarra

class PizarraSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Pizarra
    """
    class Meta:
        model = Pizarra
        fields = ('idpiz', 'nombrepiz', 'descripcionpiz', 'fechacreacion',
                  'fechafinal', 'avancepiz', 'logindueno', 'is_active')   
