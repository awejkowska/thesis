# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('InzApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dziedzina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazwa', models.CharField(max_length=255)),
                ('skrot', models.CharField(max_length=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Jezyk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazwa', models.CharField(max_length=255)),
                ('skrot', models.CharField(max_length=15)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='kolekcja',
            old_name='nazwa_kolecji',
            new_name='nazwa_kolekcji',
        ),
        migrations.RemoveField(
            model_name='publikacja',
            name='plik_lub_url',
        ),
        migrations.RemoveField(
            model_name='rodzial_ksiazki',
            name='autor',
        ),
        migrations.RemoveField(
            model_name='rodzial_ksiazki',
            name='tytul',
        ),
        migrations.RemoveField(
            model_name='uzytkownik',
            name='rola',
        ),
        migrations.AddField(
            model_name='kolekcja',
            name='czy_publiczna',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ksiazka',
            name='isbn',
            field=models.CharField(default=9871523689124L, max_length=13),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publikacja',
            name='czy_publiczna',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publikacja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 22, 18, 33, 58, 958000)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publikacja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 22, 18, 33, 58, 958000)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publikacja',
            name='ilosc_odslon',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publikacja',
            name='plik',
            field=models.FilePathField(path=b'/InzApp/files', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publikacja',
            name='url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publikacja',
            name='utworzyl',
            field=models.CharField(default='user', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publikacja',
            name='zmodyfikowal',
            field=models.ForeignKey(default='1', to='InzApp.Uzytkownik'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rodzial_ksiazki',
            name='id_ksiazki',
            field=models.ForeignKey(default='1', to='InzApp.Ksiazka'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uzytkownik',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 22, 18, 33, 58, 953000)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uzytkownik',
            name='data_ostatniego_logowania',
            field=models.DateTimeField(default=datetime.date(2015, 10, 22)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uzytkownik',
            name='data_rejestracji',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 22, 18, 33, 58, 953000)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uzytkownik',
            name='jest_administratorem',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='artykul',
            name='zakres_stron',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='autor',
            name='opis',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='data_modyfikacji',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 22, 18, 33, 58, 955000)),
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='data_utworzenia',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 22, 18, 33, 58, 954000)),
        ),
        migrations.AlterField(
            model_name='kolekcja',
            name='opis',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='dziedzina',
            field=models.ForeignKey(to='InzApp.Dziedzina'),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='jezyk',
            field=models.ForeignKey(to='InzApp.Jezyk'),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='opis',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='rodzaj',
            field=models.CharField(max_length=1, choices=[(b'K', b'Ksi\xc4\x85\xc5\xbcka'), (b'A', b'Artyku\xc5\x82'), (b'M', b'Materia\xc5\x82y konferencyjne'), (b'W', b'Witryna internetowa'), (b'R', b'Rozdzia\xc5\x82 ksi\xc4\x85\xc5\xbcki')]),
        ),
        migrations.AlterField(
            model_name='publikacja',
            name='slowa_kluczowe',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='witryna_internetowa',
            name='data_odwiedzin',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 22, 18, 33, 58, 963000)),
        ),
        migrations.AlterField(
            model_name='witryna_internetowa',
            name='wlasciciel',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
