from django.db import models

# Create your models here.

# Primer esquema de clase para pruebas
class Search(models.Model):
    keyWord = models.CharField(max_length=100)

# Esquema real para la busqueda de palabras claves
class keyWord (models.Model):
    keyWord = models.CharField(max_length=270)
