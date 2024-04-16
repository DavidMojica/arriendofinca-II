from .models import Departamento, Imagenes, Inmueble, TipoCobro, TipoDocumento, TipoInmueble, ArriendoVenta, Municipio, Usuario
from django import forms
from django.db import models

#-----Variables-----#
TEXT_SELECCIONAR = "Seleccionar..."

MAX_MB_IMAGE = 2
MAX_UPLOAD_SIZE = MAX_MB_IMAGE * 1024 * 1024
MAX_IMAGES = 5

#-------------------------------------------------
#----------------------HOME-----------------------
#-------------------------------------------------
class BusquedaInmuebleForm(forms.Form):
    tipo_inmueble = forms.ModelChoiceField(
        label="Busco un(a)",
        widget=forms.Select(attrs={'class':'form-select'}),
        queryset=TipoInmueble.objects.all(),
        empty_label=TEXT_SELECCIONAR,
        required=True
    )
    arriendo_venta = forms.ModelChoiceField(
        label="Para",
        widget=forms.Select(attrs={'class':'form-select'}),
        queryset=ArriendoVenta.objects.all(),
        empty_label=TEXT_SELECCIONAR,
        required=True
    )
    municipio = forms.ModelChoiceField(
        label="Ubicación",
        widget=forms.Select(attrs={'class':'form-select'}),
        queryset=Municipio.objects.all(),
        empty_label=TEXT_SELECCIONAR,
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
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'new_tipo_documento'}),
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
        widget=forms.CheckboxInput(attrs={'id': 'new_whatsapp'})
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
        widget=forms.TextInput(attrs={'id': 'edit_nombre', 'class': 'form-control'}),
        required=True
    )
    
    last_name = forms.CharField(
        label="Apellidos",
        widget=forms.TextInput(attrs={'id':'edit_apellidos', 'class': 'form-control'}),
        required=True
    )
    
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={ 'id': 'edit_email', 'class': 'form-control'})
    )
    
    celular = forms.CharField(
        required=True,
        label='Celular',
        widget=forms.TextInput(attrs={'id':'edit_celular', 'class': 'form-control'})
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
    password_old = forms.CharField(
        required=False,
        label="Contraseña antigua",
        widget=forms.PasswordInput(attrs={ 'id': 'edit_password_old', 'class': 'form-control', 'placeholder': 'Tu contraseña anterior'})
    )
    
    password = forms.CharField(
        required=False,
        label="Contraseña nueva",
        widget=forms.PasswordInput(attrs={ 'id': 'edit_password_1', 'class': 'form-control', 'placeholder':'Tu contraseña nueva'})
    )
    
    password2 = forms.CharField(
        required=False,
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={ 'id': 'edit_password_2', 'class': 'form-control', 'placeholder': 'Confirma tu contraseña nueva'})
    )
    
    
    class Meta:
        fields = ('password_old', 'password', 'password2')
        
#-------------------------------------------------
#-------------------Propiedades-------------------
#-------------------------------------------------
#--Filtrar propiedades desde el area de usuario
class FiltrarInmuebles(forms.Form):
    id = forms.IntegerField(
        label="ID de inmobiliario",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class':'form-control'})
    )
    
    tipo_inmueble = forms.ModelChoiceField(
        label="Tipo de inmueble",
        required=False,
        queryset=TipoInmueble.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id':'tipo_inmueble_filter'}),
        empty_label="Todos"
    )
    
    municipio = forms.ModelChoiceField(
        label="Municipio",
        required=False,
        queryset=Municipio.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id':'tipo_inmueble_filter'}),
        empty_label="Cualquiera"
    )

# --- Usuario: Crear propiedad --- #
class CrearInmuebleForm(forms.ModelForm):
    tipo_inmueble = forms.ModelChoiceField(
        label="Tipo de inmueble",
        required=True,
        queryset=TipoInmueble.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id':'tipo_inmueble_filter'}),
        empty_label= TEXT_SELECCIONAR
    )
    
    arriendo_venta = forms.ModelChoiceField(
        label="¿Arrendar o vender?",
        widget=forms.Select(attrs={'class':'form-select'}),
        queryset=ArriendoVenta.objects.all(),
        empty_label= TEXT_SELECCIONAR,
        required=True
    )
    
    precio = forms.IntegerField(
        label="Precio (en COP)",
        required=True,
        min_value=0,
        widget=forms.NumberInput()
    )
    
    tipo_cobro = forms.ModelChoiceField(
        label="Perido de cobro",
        required=True,
        queryset=TipoCobro.objects.all(),
        empty_label=TEXT_SELECCIONAR,
        widget=forms.Select(attrs={'class':'form-select'}),
    )
    
    departamento = forms.ModelChoiceField(
        label="Departamento de ubicación",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'departamento-select'}),
        queryset=Departamento.objects.all(),
        empty_label=TEXT_SELECCIONAR,
        required=True,
        initial=0
    )
    
    direccion = forms.CharField(
        label="Dirección del inmueble",
        widget=forms.TextInput(),
        required=True,
        strip=True
    )
    
    area = forms.IntegerField(
        label="Area",
        required=True,
        min_value=0,
        widget=forms.NumberInput()
    )
    
    area_construida = forms.IntegerField(
        label="Area construida",
        required=True,
        min_value=0,
        widget=forms.NumberInput()
    )
    
    habitaciones = forms.IntegerField(
        label="# de Habitaciones",
        required=True,
        min_value=0,
        widget=forms.NumberInput()
    )
    
    banios = forms.IntegerField(
        label="# de baños",
        required=True,
        min_value=0,
        widget=forms.NumberInput(),
    )
    
    description = forms.CharField(
        label="Descipcion del inmueble",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa las carácteristicas del inmueble (opcional)'}),
        max_length=500,
        strip=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['municipio_ubicacion'] = forms.ChoiceField(
            label="Municipio de ubicacion",
            choices=[],
            widget=forms.Select(attrs={'class': 'form-select', 'id':'municipio_select'}),
            required=True,
        )
    
    def clean_municipio_ubicacion(self):
        municipio_id = self.cleaned_data['municipio_ubicacion']
        try:
            municipio = Municipio.objects.get(pk=municipio_id)
            return municipio
        except Municipio.DoesNotExist:
            raise forms.ValidationError("El municipio seleccionado no es válido")
        
    class Meta:
        model = Inmueble
        fields = ('tipo_inmueble', 'arriendo_venta', 'precio', 'tipo_cobro', 'municipio_ubicacion', 'direccion', 'area', 'area_construida', 'habitaciones', 'banios', 'description')
    
    
# #----imagenes de los inmuebles----#
# class ImagenesInmuebleForm(forms.ModelForm):
#     imagenes = forms.FileField(
#         label="Subir imágenes (Hasta 5 imágenes de 2Mb cada una)",
#         widget=forms.ClearableFileInput(attrs={'multiple':True}),
#         required=False
#     )
    
#     def clean_imagenes(self):
#         uploaded_images = self.cleaned_data.get('imagenes')
#         total_images = len(uploaded_images) if uploaded_images else 0
        
#         if total_images > 5:
#             raise forms.ValidationError("No se pueden subir más de 5 imágenes")
        
#         for image in uploaded_images:
#             if image.size > 2 * 1024 * 1024:  # 2Mb en bytes
#                 raise forms.ValidationError("El tamaño de la imagen no puede ser mayor a 2Mb")
            
#         return uploaded_images

#     class Meta:
#         model = Imagenes
#         fields = ['imagenes']
