# Generated by Django 3.1.7 on 2021-05-29 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0003_remove_invoice_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='providers.provider'),
            preserve_default=False,
        ),
    ]
