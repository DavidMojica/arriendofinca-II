# Generated by Django 4.2.11 on 2024-04-28 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_solicituddestacados'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicituddestacados',
            name='estado',
            field=models.CharField(choices=[('A', 'Aceptar'), ('R', 'Rechazar')], max_length=1),
        ),
    ]
