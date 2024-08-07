from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from django.core.files.storage import default_storage

class TipoUsuario(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=25)
    
    def __str__(self):
        return self.description

class TipoDocumento(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=40)
    
    def __str__(self):
        return self.description

class TipoCobro(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=40)
    
    def temporizar(self):
        map_tiempo = ['por año', ' por mes', 'por semana', 'por día', 'por noche', 'de venta']
        return map_tiempo[self.id]
    
    def __str__(self):
        return self.description

class TipoInmueble(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=25)
    
    def singular(self):
        map_singular = ['Finca', 'Cabaña', 'Lote', 'Casa', 'Apartamento', 'Oficina', 'Consultorio', 'Hotel', 'Local', 'Apartaestudio', 'Habitación', 'Glamping']
        return map_singular[self.id]
    
    def __str__(self):
        return self.description
    
class ArriendoVenta(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=10)
    
    def __client_str__(self):
        if self.id == 0:
            return "Arrendar"
        elif self.id == 1: 
            return "Comprar"
        else:
            return "No reconocido"
    
    def __str__(self):
        return self.description
    
class Pais(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    
    def __str__(self):
        return self.description
    
class Departamento(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.description}"

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.description}"
    

# Login Model #
class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    groups = models.ManyToManyField(Group, related_name="customuser_set")
    documento = models.CharField(max_length = 20, unique = True)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_set")
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete = models.CASCADE, default = 1)
    celular = models.CharField(max_length=20, null=True, blank=True)
    permitir_whatsapp = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super(Usuario, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
# Inmuebles #
class Inmueble(models.Model):
    id = models.AutoField(primary_key=True)
    arriendo_venta = models.ForeignKey(ArriendoVenta, on_delete = models.CASCADE)
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete = models.CASCADE)
    precio = models.BigIntegerField()
    tipo_cobro = models.ForeignKey(TipoCobro, on_delete=models.CASCADE, default=1)
    municipio_ubicacion = models.ForeignKey(Municipio, on_delete = models.CASCADE, null=True, blank=True)
    direccion = models.CharField(max_length=80)
    area = models.CharField(max_length=7)
    area_construida = models.CharField(max_length=7)
    habitaciones = models.CharField(max_length=3)
    banios = models.CharField(max_length=3)
    description = models.CharField(max_length=1000)
    duenio = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class TipoCertificado(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    badge = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return f"{self.description}"

class Certificado(models.Model):
    id = models.AutoField(primary_key=True)
    inmueble = models.OneToOneField(Inmueble, on_delete=models.CASCADE, null=True, blank=True)
    fecha_certificacion = models.DateTimeField(auto_now_add=True, null=True)
    tipo = models.ForeignKey(TipoCertificado, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Inmueble: {self.inmueble.id} Ceritificado: {self.id}"

class Imagenes(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='inmuebles', null=True)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, blank=True, null=True, related_name="imagenes")
    
    def __str__(self):
        return self.id

class Destacados(models.Model):
    id = models.AutoField(primary_key=True)
    inmueble = models.OneToOneField(Inmueble, on_delete=models.CASCADE, null=True, blank=True)
    fecha_destacado = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"Inmueble: {self.inmueble.id} Id Destacado: {self.id} Fecha: {self.fecha_destacado}"

class SolicitudDestacados(models.Model):
    ESTADO_CHOICES = (
        ('A', 'Aceptar'),
        ('R', 'Rechazar'),
    )
    
    inmueble = models.OneToOneField('Inmueble', on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    
    def __str__(self):
        return f"Solicitud de destacado para inmueble: {self.inmueble.id}"

@receiver(post_save, sender=SolicitudDestacados)
def gestionar_solicitud_destacado(sender, instance, created, **kwargs):
    if instance.estado == 'A':
        Destacados.objects.create(inmueble=instance.inmueble)
        instance.delete()

    elif instance.estado == 'R':
        instance.delete()

class SolicitudCertificados(models.Model):
    ESTADO_CHOICES = (
        ('A', 'Aceptar'),
        ('R', 'Rechazar'),
    )
    
    inmueble = models.OneToOneField('Inmueble', on_delete=models.CASCADE, null=True, blank=True)
    tipo_certificado = models.ForeignKey(TipoCertificado, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    
    def __str__(self):
        return f"Solicitud de certificación para inmueble: {self.inmueble.id}"
    
@receiver(post_save, sender=SolicitudCertificados)
def gestionar_solicitud_certificado(sender, instance, created, **kwargs):
    if instance.estado == 'A':
        Certificado.objects.create(inmueble=instance.inmueble, tipo=instance.tipo_certificado)
        instance.delete()

    elif instance.estado == 'R':
        instance.delete()

@receiver(pre_delete, sender=Inmueble)
def eliminar_imagenes_inmueble(sender, instance, **kwargs):
    imagenes = Imagenes.objects.filter(inmueble=instance)
    for imagen in imagenes:
        if imagen.img:
            default_storage.delete(imagen.img.name)
        imagen.delete()
