# Generated by Django 3.1.7 on 2021-05-24 14:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('tax_registration_number', models.CharField(blank=True, max_length=50, unique=True)),
                ('society', models.CharField(blank=True, max_length=50)),
                ('telephone', models.CharField(blank=True, max_length=9, null=True, unique=True, validators=[django.core.validators.RegexValidator('6\\d{8}', 'This field is incorrect')])),
                ('fax', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('mobile', models.CharField(blank=True, max_length=9, null=True, unique=True, validators=[django.core.validators.RegexValidator('6\\d{8}', 'This field is incorrect')])),
                ('email', models.EmailField(blank=True, max_length=50, unique=True)),
                ('adresse', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Providers',
            },
        ),
    ]