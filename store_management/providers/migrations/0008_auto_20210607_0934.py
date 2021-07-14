# Generated by Django 3.1.7 on 2021-06-07 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20210607_0923'),
        ('internal_stock', '0022_auto_20210607_0923'),
        ('providers', '0007_auto_20210607_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='internal_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='internal_stock.stock', verbose_name='stock interne'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='providers.provider', verbose_name='fournisseur'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='quantite'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='yassa_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.stock', verbose_name='stock yassa'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='prenoms'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='noms'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='society',
            field=models.CharField(blank=True, max_length=50, verbose_name='societe'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='tax_registration_number',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='matricule fiscale'),
        ),
    ]