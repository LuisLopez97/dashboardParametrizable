from django.db import models

# Create your models here.


class Search(models.Model):
    keyWord = models.CharField(max_length=100)


class keyWord (models.Model):
    keyWord = models.CharField(max_length=270)
