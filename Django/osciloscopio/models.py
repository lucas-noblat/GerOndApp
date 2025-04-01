from django.db import models

# Create your models here.

class dataSource(models.Model):
    x_value = models.FloatField()
    y_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User  # Caso tenha usuários

# Modelo para armazenar os sinais inseridos pelo usuário
class Sinal(models.Model):
    TIPO_SINAL = [
        ('senoidal', 'Senoidal'),
        ('triangular', 'Triangular'),
        ('quadrada', 'Quadrada'),
        ('ruido', 'Ruído Branco'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_SINAL)
    amplitude = models.FloatField()
    frequencia = models.FloatField()
    fase = models.FloatField()
    duty_cycle = models.FloatField(null=True, blank=True)  # Apenas para onda quadrada
    duracao = models.FloatField()
    offset = models.FloatField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

# Modelo para armazenar o resultado da combinação de sinais
class SinalResultante(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    formula = models.TextField()  # Ex: "Sinal1 + Sinal2 - Sinal3"
    dados_temporais = models.JSONField()  # Lista de valores ao longo do tempo
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resultado de {self.formula}"

# Modelo para armazenar a Transformada de Fourier
class TransformadaFourier(models.Model):
    sinal = models.ForeignKey(SinalResultante, on_delete=models.CASCADE)
    frequencias = models.JSONField()  # Lista de valores de frequência
    amplitudes = models.JSONField()   # Lista de amplitudes espectrais
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FFT de {self.sinal}"

# Modelo para armazenamento de arquivos importados/exportados
class Arquivo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=[('csv', 'CSV'), ('json', 'JSON')])
    caminho_arquivo = models.FileField(upload_to='uploads/')
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Arquivo {self.tipo} de {self.usuario}"
