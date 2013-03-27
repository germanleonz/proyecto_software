from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_log.models import Accion
from app_usuarios.models import UserProfile
from app_usuarios.serializers import UserProfileSerializer

class Login(APIView):
    def post(self, request, nombre_usuario, clave, format=None):
        usuario = authenticate(username=nombre_usuario, password=clave)
        serializer = UserProfileSerializer(usuario)
        if usuario is not None:
            if usuario.is_active:
                #Se registra la accion de login del usuario
                Accion.objects.crearAccion(
                    usuario, 
                    "El usuario %s inicio sesion" % (nombre_usuario), 
                    'i')

                #   Redirigir a pagina de login correcto (ver pared)
                print "Acceso permitido para %s" % nombre_usuario
                login(request, usuario)
                #perfil = UserProfile.objects.get(user=usuario)

                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                #   Devolver un mensaje de cuenta deshabilitada
                print "La cuenta del usuario esta deshabilitada"
                pass
        else:
            #   Devolver un mensaje de usuario o contrasena incorrectas
            print "Acceso denegado para %s" % nombre_usuario
            #   Aqui se deben levantar los errores
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileList(APIView):
    def get(self, request, format=None):
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDetail(APIView):
    def get_object(self, pk):
        try:
            return UserProfile.objects.get(id=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_profile = self.get_object(pk)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user_profile = self.get_object(pk)
        serializer = UserProfileSerializer(user_profile, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user_profile = self.get_object(pk)
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
