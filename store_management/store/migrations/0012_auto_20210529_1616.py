# Generated by Django 3.1.7 on 2021-05-29 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20210529_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='material_status',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Material Defectuous'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='material_status',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Material Defectuous'),
        ),
    ]
