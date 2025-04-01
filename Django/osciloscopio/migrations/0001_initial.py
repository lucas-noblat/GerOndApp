# Generated by Django 5.1.7 on 2025-04-01 16:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='dataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_value', models.FloatField()),
                ('y_value', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('csv', 'CSV'), ('json', 'JSON')], max_length=10)),
                ('caminho_arquivo', models.FileField(upload_to='uploads/')),
                ('data_upload', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('senoidal', 'Senoidal'), ('triangular', 'Triangular'), ('quadrada', 'Quadrada'), ('ruido', 'Ruído Branco')], max_length=10)),
                ('amplitude', models.FloatField()),
                ('frequencia', models.FloatField()),
                ('fase', models.FloatField()),
                ('duty_cycle', models.FloatField(blank=True, null=True)),
                ('duracao', models.FloatField()),
                ('offset', models.FloatField()),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SinalResultante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formula', models.TextField()),
                ('dados_temporais', models.JSONField()),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransformadaFourier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequencias', models.JSONField()),
                ('amplitudes', models.JSONField()),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('sinal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osciloscopio.sinalresultante')),
            ],
        ),
    ]
