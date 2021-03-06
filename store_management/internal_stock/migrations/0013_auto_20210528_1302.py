# Generated by Django 3.1.7 on 2021-05-28 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal_stock', '0012_auto_20210521_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='issue_quantity',
            field=models.PositiveIntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='receive_quantity',
            field=models.PositiveIntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='reorder_level',
            field=models.PositiveIntegerField(blank=True, default='0', null=True),
        ),
    ]
