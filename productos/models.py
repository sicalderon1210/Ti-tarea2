from django.db import models

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=400)


class Hamburguesa(models.Model):
    nombre = models.CharField(max_length=225)
    precio  = models.IntegerField()
    descripcion = models.CharField(max_length=400)
    imagen = models.CharField(max_length=400)
    ingredientes = models.ManyToManyField('Ingrediente', related_name='hamburguesas', blank=True)

    def __str__(self):
        return self.nombre