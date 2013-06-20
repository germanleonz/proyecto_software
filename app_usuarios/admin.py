from django.contrib import admin
from django.contrib.auth.models import User
from app_usuarios.models import UserProfile

#class UserInline(admin.StackedInline):
    #"""docstring for UserInline"""
    #model = User 

#class UserProfileAdmin(admin.ModelAdmin):
    #"""docstring for UserProfileAdmin"""
    #inlines = [UserInline] 

admin.site.register(UserProfile)
