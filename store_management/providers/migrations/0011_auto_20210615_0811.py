# Generated by Django 3.1.7 on 2021-06-15 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internal_stock', '0023_stock_provider'),
        ('store', '0017_auto_20210607_0923'),
        ('providers', '0010_auto_20210613_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='internal_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='internal_stock.stock', verbose_name='stock interne'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='yassa_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.stock', verbose_name='stock yassa'),
        ),
    ]
