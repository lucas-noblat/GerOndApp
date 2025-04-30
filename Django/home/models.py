from django.db import models

# Create your models here.

from django.contrib.auth.models import User  # Caso tenha usuários

class Sinal(models.Model):
    amplitude = models.FloatField()
    frequencia = models.FloatField()
    duracao = models.FloatField()
    offset = models.FloatField()
    
    