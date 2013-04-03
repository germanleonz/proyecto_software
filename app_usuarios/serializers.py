from django.contrib.auth.models import User

from rest_framework import serializers

from app_usuarios.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    telefono = serializers.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email',) 
