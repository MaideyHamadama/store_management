# Generated by Django 3.1.7 on 2021-05-29 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0002_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='provider',
        ),
    ]
