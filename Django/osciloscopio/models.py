from django.db import models

# Create your models here.

class dataSource(models.Model):
    x_value = models.FloatField()
    y_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)