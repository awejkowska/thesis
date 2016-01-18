# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('InzApp', '0009_auto_20160118_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artykul',
            name='czasopismo',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='autor',
            name='opis',
            field=models.CharField(max_length=5000, blank=True),
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 40, 28, 525000)),
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 40, 28, 525000)),
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='opis',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='ksiazka',
            name='wydawnictwo',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='materialy_konferencyjne',
            name='nazwa_konferencji',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 40, 28, 535000)),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 40, 28, 535000)),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='opis',
            field=models.CharField(max_length=5000, blank=True),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='tytul',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='uzytkownik',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 40, 28, 525000)),
        ),
        migrations.AlterField(
            model_name='uzytkownik',
            name='data_rejestracji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 40, 28, 525000)),
        ),
    ]
