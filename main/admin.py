from django.contrib import admin
from .models import Certificado, Inmueble

# Register your models here.
class CertificadoAdmin(admin.ModelAdmin):
    search_fields = ['id', 'inmueble']
admin.site.register(Certificado)

class InmuebleAdmin(admin.ModelAdmin):
    search_fields = ['id']
admin.site.register(Inmueble, InmuebleAdmin)

