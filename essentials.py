from django.core.exceptions import ValidationError

# Constantes # 
IMG_MAX_SIZE = 2 #Mb
KYLOBYTE = 1024

# Funciones #
def validate_file_size(value):
    filesize = value.size
    
    if filesize > IMG_MAX_SIZE * KYLOBYTE * KYLOBYTE:
        raise ValidationError(f"El tamaño del archivo permitido es {IMG_MAX_SIZE} MB")
    