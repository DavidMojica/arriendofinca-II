from .models import TipoDocumento, TipoInmueble, ArriendoVenta, Municipio, Usuario
from django import forms
from django.db import models

#-------------------------------------------------
#----------------------HOME-----------------------
#-------------------------------------------------
class BusquedaInmuebleForm(forms.Form):
    tipo_inmueble = forms.ModelChoiceField(
        label="Busco un(a)",
        widget=forms.Select(attrs={'class':'form-select'}),
        queryset=TipoInmueble.objects.all(),
        empty_label="Seleccionar",
        required=True
    )
    arriendo_venta = forms.ModelChoiceField(
        label="Para",
        widget=forms.Select(attrs={'class':'form-select'}),
        queryset=ArriendoVenta.objects.all(),
        empty_label="Seleccionar",
        required=True
    )
    municipio = forms.ModelChoiceField(
        label="Ubicación",
        widget=forms.Select(attrs={'class':'form-select'}),
        queryset=Municipio.objects.all(),
        empty_label="Seleccionar",
        required=True
    )
    solo_certificados = forms.BooleanField(
        label="Sólo inmuebles certificados",
        widget=forms.CheckboxInput(),
        required=False
    )

#-------------------------------------------------
#----------------------LOGIN----------------------
#-------------------------------------------------
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        required=True,
        widget=forms.TextInput(attrs={'id':'username'})
    )

    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget= forms.PasswordInput(attrs={'id':'password'})
    )

    class Meta:
        fields = ('username', 'password')

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={'id': 'new_nombre'}),
        required=True
    )
    
    last_name = forms.CharField(
        label="Apellidos",
        widget=forms.TextInput(attrs={'id':'new_apellidos'}),
        required=True
    )
    documento = forms.CharField(
        required=True,
        label="Documento",
        widget=forms.TextInput(attrs={'id':'new_documento'})
    )
    tipo_documento = forms.ModelChoiceField(
        label="Tipo de documento",
        widget=forms.Select(attrs={'class': 'form-select'}),
        queryset=TipoDocumento.objects.all(),
        empty_label="Tipo documento",
        required=True
    )

    username=forms.CharField(
        required=True,
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'id':'new_username'})
    )
    
    password = forms.CharField(
        required=True,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={ 'id': 'new_password'})
    )

    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={ 'id': 'new_email'})
    )
    
    celular = forms.CharField(
        required=True,
        label='Celular',
        widget=forms.TextInput(attrs={'id':'new_celular'})
    )
    
    permitir_whatsapp = forms.BooleanField(
        label="Permitir contacto por WhatsApp",
        required=False,
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'documento', 'tipo_documento', 'username', 'password', 'email', 'celular', 'permitir_whatsapp')

#-------------------------------------------------
#-------------------EDIT ACCOUNT------------------
#-------------------------------------------------
class EditAccountBasics(forms.ModelForm):
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={'id': 'edit_nombre'}),
        required=True
    )
    
    last_name = forms.CharField(
        label="Apellidos",
        widget=forms.TextInput(attrs={'id':'edit_apellidos'}),
        required=True
    )
    
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={ 'id': 'edit_email'})
    )
    
    celular = forms.CharField(
        required=True,
        label='Celular',
        widget=forms.TextInput(attrs={'id':'edit_celular'})
    )
    
    permitir_whatsapp = forms.BooleanField(
        label="Permitir contacto por WhatsApp",
        required=False,
        widget=forms.CheckboxInput()
    )
    
    class Meta:
        model=Usuario
        fields = ('first_name', 'last_name', 'email', 'celular', 'permitir_whatsapp')
       
class EditAccountDangerZone(forms.Form):
    username=forms.CharField(
        required=True,
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'id':'edit_username'})
    )
    
    password_old = forms.CharField(
        required=False,
        label="Contraseña antigua",
        widget=forms.PasswordInput(attrs={ 'id': 'edit_password_old'})
    )
    
    password = forms.CharField(
        required=False,
        label="Contraseña nueva",
        widget=forms.PasswordInput(attrs={ 'id': 'edit_password_1'})
    )
    
    password2 = forms.CharField(
        required=False,
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={ 'id': 'edit_password_2'})
    )
    
    class Meta:
        fields = ('username', 'password_old', 'password', 'password2')