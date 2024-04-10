from .models import TipoInmueble, ArriendoVenta, Municipio, Usuario
from django import forms
from django.db import models

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
        widget=forms.CheckboxInput(attrs={'class': ''}),
        required=False
    )

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
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del empleado/administrador', 'id': 'nombre'})
    )
    
    last_name = forms.CharField(
        label="Apellidos",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese los apellidos', 'id':'apellidos'})
    )

    username=forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Documento del usuario', 'id':'documento'})
    )
    
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña', 'id': 'password'})
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Correo electrónico', 'id': 'email'})
    )

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'password')
