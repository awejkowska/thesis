# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('InzApp', '0002_auto_20151022_1834'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rodzial_Ksiazki',
            new_name='Rozdzial_Ksiazki',
        ),
        migrations.AddField(
            model_name='artykul',
            name='nr_czasopisma',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ksiazka',
            name='miejsce_wydania',
            field=models.CharField(default='Warszawa', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='materialy_konferencyjne',
            name='lokalizacja_konferencji',
            field=models.CharField(default='Wydzia\u0142 Informatyki Politechniki Bia\u0142ostockiej', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 15, 8, 10, 646000)),
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 15, 8, 10, 646000)),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 15, 8, 10, 653000)),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 15, 8, 10, 653000)),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='plik',
            field=models.FileField(null=True, upload_to=b'files/', blank=True),
        ),
        migrations.AlterField(
            model_name='uzytkownik',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 15, 8, 10, 644000)),
        ),
        migrations.AlterField(
            model_name='uzytkownik',
            name='data_rejestracji',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 15, 8, 10, 644000)),
        ),
        migrations.AlterField(
            model_name='witryna_internetowa',
            name='data_odwiedzin',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 15, 8, 10, 662000)),
        ),
    ]
