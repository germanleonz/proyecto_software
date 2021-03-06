from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_pizarras.models import Pizarra, obtener_pizarras
from app_pizarras.serializers import PizarraSerializer

class PizarraList(APIView):
    def get(self, request, username, format=None):
        usuario = User.objects.get(username=username)
        pizarras = obtener_pizarras(usuario)
        serializer = PizarraSerializer(pizarras, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PizarraSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PizarraDetail(APIView):
    def get_object(self, pk):
        try:
            return Pizarra.objects.get(idpiz=pk)
        except Pizarra.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pizarra = self.get_object(pk)
        serializer = PizarraSerializer(pizarra)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        pizarra = self.get_object(pk)
        serializer = PizarraSerializer(pizarra, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pizarra = self.get_object(pk)
        pizarra.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

