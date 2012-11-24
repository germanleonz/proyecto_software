from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from app_usuario.models import MiUsuario

#class UserCreationForm(forms.ModelForm):
    #"""
    #Formulario para crear nuevos usuarios. Incluye todos los campos 
    #requeridos, mas un campo de contrasena repetido
    #"""
    #password1 = forms.CharField(label='Contrasena', widget=forms.PasswordInput)
    #password2 = forms.CharField(label='Confirme contrasena', widget=forms.PasswordInput)

    #class Meta:
        #model = MiUsuario
        #fields = ('nombre_usuario', 'correo', 'nombre', 'apellido', 'nombre_empresa')

    #def clean_password2(self):
        #"""
        #Chequear que las dos contrasenas coinciden
        #"""
        #password1 = self.cleaned_data.get("password1")
        #password2 = self.cleaned_data.get("password2")
        #if password1 and password2 and password1 != password2:
            #raise forms.ValidationError("Las contrasenas no coinciden")
        #return password2

    #def save(self, commit=True):
        #"""
        #Salva la contrasena provista en formato de hash
        #"""
        #user = super(UserCreationForm, self).save(commit=False)
        #user.set_password(self.cleaned_data["password1"])
        #if commit:
            #user.save()
        #return user

#class UserChangeForm(forms.ModelForm):
    #"""
    #Un form para actualizar a los usuarios. Incluye todos los campos del usuario,
    #pero reemplaza la contrasena con el hash de la contrasena (TEMPORAL)
    #"""
    #password = ReadOnlyPasswordHashField()

    #class Meta:
        #model = MiUsuario

#class MiAdminUser(UserAdmin):
    ##   Las formas para agregar y cambiar instancias de usuarios
    #form = UserChangeForm
    #add_form = UserCreationForm

    ##   Los campos para ser usados en mostrar el User model
    ##   Estas override la definicion en el UserAdmin base
    ##   que referencian campos especificos de app_usuarios.User
    #list_display = ('nombre_usuario', 'correo', 'is_admin')
    #list_filter = ('is_admin')
    #fieldsets = (
            #(None, {'fields': ('nombre_usuario', 'password')}),
            #('Informacion personal', {'fields': ('nombre', 'apellido',)}),
            #('Permisos', {'fields': ('is_admin',)}),
            #('Fechas importantes', {'fields':('last_login')}),
    #)
    #addfieldsets = (
        #(None, {
            #'classes': ('wide',),
            #'fields': ('correo', 'nombre_empresa', 'password1', 'password2')}
        #),
    #)
    #search_fields = ('nombre_usuario',)
    #ordering = ('nombre_usuario')
    #filter_horizontal = ()

#   Ahora registramos el nuevo UserAdmin
admin.site.register(UserProfile)

##   Define an inline admin descriptor for UserProfile model
##   which acts a bit like a singleton
#class UserProfileInline(admin.StackedInline):
    #model = MiUsuario
    #can_delete = False
    #verbose_name_plural = 'profile'

##   Definir un nuevo UserAdmin
#class UserAdmin(UserAdmin):
    #inlines = (UserProfileInline, )

##   Re-register UserAdmin
#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)

###admin.site.register(Poll)
