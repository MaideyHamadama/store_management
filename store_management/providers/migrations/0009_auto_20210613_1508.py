# Generated by Django 3.1.7 on 2021-06-13 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0008_auto_20210607_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='internal_stock',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='yassa_stock',
        ),
    ]