from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from essentials import validate_file_size

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
        map_tiempo = {0: 'Año', 1: 'Mes', 2: 'Semana', 3: 'Dia', 4:'Noche'}
        return map_tiempo[self.id]
    
    def __str__(self):
        return self.description

class TipoInmueble(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=25)
    
    def __str__(self):
        return self.description
    
class ArriendoVenta(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=10)
    
    def __str__(self):
        return self.description
    
class Certificado(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    description = models.CharField(max_length=25)
    
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
        return self.description

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.departamento} - {self.description} - {self.departamento.pais}"
    

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
    precio = models.CharField(max_length=20)
    tipo_cobro = models.ForeignKey(TipoCobro, on_delete=models.CASCADE, default=1)
    municipio_ubicacion = models.ForeignKey(Municipio, on_delete = models.CASCADE)
    direccion = models.CharField(max_length=80)
    area = models.CharField(max_length=7)
    area_construida = models.CharField(max_length=7)
    habitaciones = models.CharField(max_length=3)
    banios = models.CharField(max_length=3)
    description = models.CharField(max_length=300)
    duenio = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    certificado = models.ForeignKey(Certificado, on_delete=models.CASCADE, null=True, blank=True)

class Imagenes(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='inmuebles_img')
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.id


