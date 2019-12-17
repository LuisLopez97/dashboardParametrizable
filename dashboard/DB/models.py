from django.db import models


class Busquedas(models.Model):
    lenguaje = models.CharField(max_length=100)
    palabraclave = models.CharField(max_length=140)
    cantidadtweets = models.IntegerField()
    fechadebusqueda = models.DateTimeField(auto_now_add=True)
    # Create your models here.
