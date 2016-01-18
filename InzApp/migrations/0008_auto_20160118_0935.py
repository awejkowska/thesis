# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('InzApp', '0007_auto_20160116_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kolekcja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 35, 46, 155000)),
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 35, 46, 155000)),
        ),
        migrations.AlterField(
            model_name='ksiazka',
            name='format',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='ksiazka',
            name='ilosc_stron',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='ksiazka',
            name='isbn',
            field=models.CharField(max_length=13, blank=True),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 35, 46, 165000)),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 35, 46, 165000)),
        ),
        migrations.AlterField(
            model_name='uzytkownik',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 35, 46, 155000)),
        ),
        migrations.AlterField(
            model_name='uzytkownik',
            name='data_rejestracji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 9, 35, 46, 155000)),
        ),
        migrations.AlterField(
            model_name='witryna_internetowa',
            name='data_odwiedzin',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
