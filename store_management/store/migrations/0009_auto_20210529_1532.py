# Generated by Django 3.1.7 on 2021-05-29 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20210529_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='material_status',
        ),
        migrations.RemoveField(
            model_name='stockhistory',
            name='material_status',
        ),
    ]