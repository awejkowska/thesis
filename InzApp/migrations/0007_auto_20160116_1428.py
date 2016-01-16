# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('InzApp', '0006_auto_20160116_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kolekcja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 14, 28, 31, 45000)),
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 14, 28, 31, 45000)),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 14, 28, 31, 54000)),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 14, 28, 31, 54000)),
        ),
        migrations.AlterField(
            model_name='uzytkownik',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 14, 28, 31, 43000)),
        ),
        migrations.AlterField(
            model_name='uzytkownik',
            name='data_rejestracji',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 14, 28, 31, 43000)),
        ),
        migrations.AlterField(
            model_name='witryna_internetowa',
            name='data_odwiedzin',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 14, 28, 31, 64000)),
        ),
    ]
