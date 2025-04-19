from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)  # importante hashearla luego
    imagen = models.ImageField(upload_to='rostros/')  # se guarda en media/rostros/