# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('InzApp', '0003_auto_20151210_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='uzytkownik',
            name='zablokowany',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 9, 1, 36, 25, 727000)),
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 9, 1, 36, 25, 727000)),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 9, 1, 36, 25, 727000)),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 9, 1, 36, 25, 727000)),
        ),
        migrations.AlterField(
            model_name='uzytkownik',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 9, 1, 36, 25, 727000)),
        ),
        migrations.AlterField(
            model_name='uzytkownik',
            name='data_rejestracji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 9, 1, 36, 25, 727000)),
        ),
        migrations.AlterField(
            model_name='witryna_internetowa',
            name='data_odwiedzin',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 9, 1, 36, 25, 737000)),
        ),
    ]
