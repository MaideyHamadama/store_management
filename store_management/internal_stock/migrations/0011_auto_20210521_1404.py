# Generated by Django 3.1.7 on 2021-05-21 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal_stock', '0010_auto_20210521_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='quantity',
            field=models.IntegerField(blank=True, default='0', null=True, unique=True),
        ),
    ]
