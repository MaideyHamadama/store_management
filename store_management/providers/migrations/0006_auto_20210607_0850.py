# Generated by Django 3.1.7 on 2021-06-07 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0005_auto_20210529_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='total_ht',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_ttc',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_tva',
            field=models.PositiveBigIntegerField(),
        ),
    ]
