# Generated by Django 3.1.7 on 2021-05-28 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210528_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='material_status',
            field=models.BooleanField(blank=True, null=True, verbose_name='Material Defectuous'),
        ),
    ]
