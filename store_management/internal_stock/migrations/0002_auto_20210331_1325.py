# Generated by Django 3.1.7 on 2021-03-31 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal_stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='material_status',
            field=models.BooleanField(blank=True, null=True, verbose_name='Material defectuous'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='date_created',
            field=models.DateTimeField(),
        ),
    ]