# Generated by Django 3.1.7 on 2021-03-31 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='category',
        ),
        migrations.RemoveField(
            model_name='stockhistory',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
