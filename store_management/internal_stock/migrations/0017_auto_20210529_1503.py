# Generated by Django 3.1.7 on 2021-05-29 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal_stock', '0016_auto_20210528_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='material_status',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Material Defectuous'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='material_status',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Material Defectuous'),
        ),
    ]
