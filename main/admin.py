from django.contrib import admin
from .models import Certificado, Inmueble, Destacados, Usuario, SolicitudDestacados

# Register your models here.
class CertificadoAdmin(admin.ModelAdmin):
    search_fields = ['id', 'inmueble']
admin.site.register(Certificado, CertificadoAdmin)

class InmuebleAdmin(admin.ModelAdmin):
    search_fields = ['id']
admin.site.register(Inmueble, InmuebleAdmin)

class DestacadosAdmin(admin.ModelAdmin):
    search_fields = ['id']
admin.site.register(Destacados, DestacadosAdmin)

class UsuariosAdmin(admin.ModelAdmin):
    search_fields = ['id', 'first_name', 'last_name']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    get_full_name.admin_order_field = 'first_name' 
    get_full_name.short_description = 'Nombre Completo'
    
admin.site.register(Usuario, UsuariosAdmin)

class SolicitudesDestacadosAdmin(admin.ModelAdmin):
    search_fields = ['id']
    
admin.site.register(SolicitudDestacados, SolicitudesDestacadosAdmin)
