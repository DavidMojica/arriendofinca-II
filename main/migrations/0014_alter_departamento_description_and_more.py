# Generated by Django 4.2.11 on 2024-04-15 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_municipio_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamento',
            name='description',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='municipio',
            name='description',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='pais',
            name='description',
            field=models.CharField(max_length=50),
        ),
    ]