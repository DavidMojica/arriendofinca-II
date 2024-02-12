from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager

class TipoUsuario(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=25)
    
    def __str__(self):
        return self.desc


# Login Model #
class usuario(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="customuser_set")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_set")
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete = models.CASCADE, default = 1)
    
    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super(usuario, self).save(*args, **kwargs)

