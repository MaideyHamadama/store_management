# Generated by Django 3.1.7 on 2021-06-07 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20210607_0713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='back_to_usine',
            field=models.BooleanField(blank=True, null=True, verbose_name='retour en usine'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='issue_by',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='emis par'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='issue_quantity',
            field=models.IntegerField(blank=True, default='0', null=True, verbose_name='quantite emise'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='issue_to',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='emis a'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='item_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='article'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='quantity',
            field=models.IntegerField(blank=True, default='0', null=True, verbose_name='quantite'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='receive_by',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='recu par'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='receive_quantity',
            field=models.IntegerField(blank=True, default='0', null=True, verbose_name='quantite recu'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='reorder_level',
            field=models.IntegerField(blank=True, default='0', null=True, verbose_name='niveau de seuil'),
        ),
    ]
