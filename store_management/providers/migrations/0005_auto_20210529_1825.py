# Generated by Django 3.1.7 on 2021-05-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0004_invoice_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='total_ht',
            field=models.PositiveBigIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_ttc',
            field=models.PositiveBigIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_tva',
            field=models.PositiveBigIntegerField(blank=True),
        ),
    ]