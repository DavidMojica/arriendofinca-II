# Generated by Django 4.2.11 on 2024-04-11 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_desc_arriendoventa_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='celular',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='permitir_whatsapp',
            field=models.BooleanField(default=False),
        ),
    ]
