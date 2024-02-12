from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from essentials import validate_file_size

class TipoUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=25)
    
    
    def __str__(self):
        return self.desc

class TipoDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=20)
    
    def __str__(self):
        return self.desc

class TipoInmueble(models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=25)
    
    def __str__(self):
        return self.desc
    
class ArriendoVenta(models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=10)
    
    def __str__(self):
        return self.desc
    
class Certificado(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    desc = models.CharField(max_length=25)
    
    def __str__(self):
        return self.desc

class Pais(models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=10)
    
    def __str__(self):
        return self.desc
    
class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=10)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.desc

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=10)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.desc
    
class Imagenes(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='images/', validators=[validate_file_size])
    
    def __str__(self):
        return self.id


# Login Model #
class Usuario(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="customuser_set")
    documento = models.CharField(max_length = 20, unique = True)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_set")
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete = models.CASCADE, default = 1)
    nombre = models.EmailField()
    email = models.CharField(max_length = 50)
    fecha_nacimiento = models.DateField()
    
    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super(Usuario, self).save(*args, **kwargs)
        
# Inmuebles #
class Inmueble(models.Model):
    id = models.AutoField(primary_key=True)
    arriendo_venta = models.ForeignKey(ArriendoVenta, on_delete = models.CASCADE)
    municipio_ubicacion = models.ForeignKey(Municipio, on_delete = models.CASCADE)
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete = models.CASCADE)
    precio = models.CharField(max_length=20)
    direccion = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=300)
    duenio = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    area = models.CharField(max_length=7)
    area_construida = models.CharField(max_length=7)
    habitaciones = models.CharField(max_length=3)
    banios = models.CharField(max_length=3)
    certificado = models.ForeignKey(Certificado, on_delete=models.CASCADE)

# Many to many #
class InmuebleImg(models.Model):
    id_img = models.ForeignKey(Imagenes, on_delete=models.CASCADE)
    id_inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)

