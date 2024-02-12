from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager

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
        
        

