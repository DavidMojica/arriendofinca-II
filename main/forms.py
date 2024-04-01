from .models import TipoInmueble, ArriendoVenta, Municipio
from django import forms
from django.db import models

class BusquedaInmuebleForm(forms.Form):
    tipo_inmueble = forms.ModelChoiceField(
        label="Busco un(a): ",
        widget=forms.Select(attrs={'class':'form-select'}),
        queryset=TipoInmueble.objects.all(),
        empty_label="Seleccionar",
        required=True
    )
    arriendo_venta = forms.ModelChoiceField(
        label="para: ",
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
        label="Buscar sólo inmuebles certificados",
        widget=forms.CheckboxInput(attrs={'class': 'green-switch'}),
        required=False
    )