# Generated by Django 3.1.7 on 2021-05-26 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internal_stock', '0012_auto_20210521_1405'),
        ('store', '0002_auto_20210331_1520'),
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('total_ht', models.CharField(blank=True, max_length=20)),
                ('total_tva', models.CharField(blank=True, max_length=20)),
                ('total_ttc', models.CharField(blank=True, max_length=20)),
                ('internal_stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='internal_stock.stock')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='providers.provider')),
                ('yassa_stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.stock')),
            ],
            options={
                'verbose_name_plural': 'Invoices',
            },
        ),
    ]