from django.db import models

# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

class ClusterGenero(models.Model):
    llave = models.CharField(max_length=15)
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=300)
    identificador = models.BooleanField(default=True)
    fecha_y_hora = models.DateTimeField()

