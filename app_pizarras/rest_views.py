from app_pizarras.models import Pizarra
from app_pizarras.serializers import PizarraSerializer
from rest_framework import generics

class PizarraList(generics.ListCreateAPIView):
    model = Pizarra
    serializer_class = PizarraSerializer

class PizarraDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Pizarra
    serializer_class = PizarraSerializer
