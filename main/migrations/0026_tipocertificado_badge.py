# Generated by Django 4.2.11 on 2024-04-28 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_solicituddestacados_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipocertificado',
            name='badge',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
