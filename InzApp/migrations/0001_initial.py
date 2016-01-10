# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artykul',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_publikacji', models.DateField()),
                ('czasopismo', models.CharField(max_length=255)),
                ('zakres_stron', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imie', models.CharField(max_length=255)),
                ('nazwisko', models.CharField(max_length=255)),
                ('opis', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kolekcja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazwa_kolecji', models.CharField(max_length=255)),
                ('opis', models.CharField(max_length=255)),
                ('data_utworzenia', models.DateTimeField()),
                ('data_modyfikacji', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kolekcja_Publikacja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_kolekcji', models.ForeignKey(to='InzApp.Kolekcja')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ksiazka',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_wydania', models.DateField()),
                ('wydawnictwo', models.CharField(max_length=255)),
                ('format', models.CharField(max_length=50)),
                ('ilosc_stron', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Materialy_Konferencyjne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazwa_konferencji', models.CharField(max_length=255)),
                ('data_konferencji', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publikacja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tytul', models.CharField(max_length=255)),
                ('rodzaj', models.CharField(max_length=2, choices=[(b'K', b'Ksiazka'), (b'A', b'Artykul'), (b'MK', b'Materialy konferencyjne'), (b'WI', b'Witryna internetowa'), (b'RK', b'Rozdzial ksiazki')])),
                ('dziedzina', models.CharField(max_length=3, choices=[(b'HUM', b'humanistyczne'), (b'TEO', b'teologiczne'), (b'SPO', b'spoleczne'), (b'EKO', b'ekonomiczne'), (b'PRA', b'prawne'), (b'MED', b'medyczne'), (b'MAT', b'matematyczne'), (b'CHE', b'chemiczne'), (b'FIZ', b'fizyczne'), (b'PRZ', b'przyrodnicze'), (b'TEC', b'techniczne'), (b'ROL', b'rolnicze')])),
                ('slowa_kluczowe', models.CharField(max_length=255)),
                ('plik_lub_url', models.CharField(max_length=255)),
                ('jezyk', models.CharField(max_length=255)),
                ('opis', models.CharField(max_length=255)),
                ('autor', models.ForeignKey(to='InzApp.Autor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rodzial_Ksiazki',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tytul', models.CharField(max_length=255)),
                ('autor', models.CharField(max_length=255)),
                ('id_publikacji', models.ForeignKey(to='InzApp.Publikacja')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uzytkownik',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login', models.CharField(max_length=50)),
                ('haslo', models.CharField(max_length=50)),
                ('rola', models.CharField(max_length=1, choices=[(b'1', b'User'), (b'2', b'Admin')])),
                ('email', models.EmailField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Witryna_Internetowa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wlasciciel', models.CharField(max_length=255)),
                ('adres_URL', models.CharField(max_length=255)),
                ('data_odwiedzin', models.DateTimeField()),
                ('id_publikacji', models.ForeignKey(to='InzApp.Publikacja')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='materialy_konferencyjne',
            name='id_publikacji',
            field=models.ForeignKey(to='InzApp.Publikacja'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ksiazka',
            name='id_publikacji',
            field=models.ForeignKey(to='InzApp.Publikacja'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kolekcja_publikacja',
            name='id_publikacji',
            field=models.ForeignKey(to='InzApp.Publikacja'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kolekcja',
            name='id_uzytkownika',
            field=models.ForeignKey(to='InzApp.Uzytkownik'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='artykul',
            name='id_publikacji',
            field=models.ForeignKey(to='InzApp.Publikacja'),
            preserve_default=True,
        ),
    ]
