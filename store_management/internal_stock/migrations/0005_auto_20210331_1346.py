# Generated by Django 3.1.7 on 2021-03-31 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal_stock', '0004_auto_20210331_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='date_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='last_updated',
            field=models.DateTimeField(null=True),
        ),
    ]