# coding=utf-8
from django.db import models
from datetime import datetime
import datetime

# Create your models here.
class Uzytkownik(models.Model):
    login = models.CharField(max_length=50) 
    haslo = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    jest_administratorem = models.BooleanField(default=False)
    data_rejestracji = models.DateTimeField(default=datetime.datetime.now())
    data_modyfikacji = models.DateTimeField(default=datetime.datetime.now())
    data_ostatniego_logowania = models.DateTimeField()
    zablokowany = models.BooleanField(default=False)
    def __str__(self):
	    return "Użytkownik: "+self.login.encode('utf8')+" ("+self.email.encode('utf8')+")"
    
class Kolekcja(models.Model):
    nazwa_kolekcji = models.CharField(max_length=255)
    opis = models.CharField(max_length=5000)
    data_utworzenia = models.DateTimeField(default=datetime.datetime.now()) 
    data_modyfikacji = models.DateTimeField(default=datetime.datetime.now()) 
    czy_publiczna = models.BooleanField(default=False)
    id_uzytkownika = models.ForeignKey(Uzytkownik) # --- FK --- #
    # pole = models.ForeignKey(innaKlasa)
    # CharField / DateField / IntegerField
    def __str__(self):
	    return self.nazwa_kolekcji.encode('utf8')+", utworzono: "+str(self.data_utworzenia)+", zmodyfikowano: "+str(self.data_modyfikacji)+"; "+self.opis.encode('utf8')+" ["+str(self.id_uzytkownika)+"]"
	
class Autor(models.Model):
    imie = models.CharField(max_length=255)
    nazwisko = models.CharField(max_length=255)
    opis = models.CharField(max_length=5000, blank=True) #not required
    def __str__(self):
        if self.opis == "":
            return self.imie.encode('utf8')+" "+self.nazwisko.encode('utf8')
        else:
            return self.imie.encode('utf8')+" "+self.nazwisko.encode('utf8')+" ("+self.opis.encode('utf8')+")"

class Dziedzina(models.Model):
    nazwa = models.CharField(max_length=255)
    skrot = models.CharField(max_length=3)
    def __str__(self):
	    return "nauki "+self.nazwa.encode('utf8')

class Jezyk(models.Model):
    nazwa = models.CharField(max_length=255)
    skrot = models.CharField(max_length=15)	
    def __str__(self):
	    return self.nazwa.encode('utf8')

class Publikacja(models.Model):
    RODZAJE = ( # ----------------- p.rodzaj / p.get_rodzaj_display()
        ('K','Książka'),
        ('A','Artykuł'),
        ('M','Materiały konferencyjne'),
        ('W','Witryna internetowa'),
        ('R','Rozdział książki'),
    )
    '''
    DZIEDZINY = (
        ('HUM','humanistyczne'),
        ('TEO','teologiczne'),
        ('SPO','spoleczne'),
        ('EKO','ekonomiczne'),
        ('PRA','prawne'),
        ('MED','medyczne'),
        ('MAT','matematyczne'),
        ('CHE','chemiczne'),
        ('FIZ','fizyczne'),
        ('PRZ','przyrodnicze'),
        ('TEC','techniczne'),
        ('ROL','rolnicze'),
    )
    '''
    tytul = models.CharField(max_length=500)
    autor = models.ForeignKey(Autor) # --- FK --- #
    rodzaj = models.CharField(max_length=1, choices=RODZAJE) 
    dziedzina = models.ForeignKey(Dziedzina) # --- FK --- # 
    jezyk  = models.ForeignKey(Jezyk) # --- FK --- # 
    opis = models.CharField(max_length=5000, blank=True) #not required
    slowa_kluczowe = models.CharField(max_length=255, blank=True) #not required
    czy_publiczna = models.BooleanField(default=False)
    utworzyl = models.CharField(max_length=50) # --- fake FK (login) --- #
    zmodyfikowal = models.ForeignKey(Uzytkownik) # --- FK --- #
    data_utworzenia = models.DateTimeField(default=datetime.datetime.now()) 
    data_modyfikacji = models.DateTimeField(default=datetime.datetime.now())
    url = models.URLField(null=True, blank=True) #not required
    plik = models.FileField(upload_to='InzApp/static/files/', null=True, blank=True) #not required
    def __str__(self):
	    return self.tytul.encode('utf8')+" / "+str(self.autor)

class Kolekcja_Publikacja(models.Model):
    id_kolekcji = models.ForeignKey(Kolekcja) # --- FK --- #
    id_publikacji = models.ForeignKey(Publikacja) # --- FK --- #
    def __str__(self):
	    return "K "+str(self.id_kolekcji.nazwa_kolekcji)+" - P "+str(self.id_publikacji.tytul)+" "+str(self.id_publikacji.autor.imie)+" "+str(self.id_publikacji.autor.nazwisko)

class Ksiazka(models.Model):
    id_publikacji = models.ForeignKey(Publikacja) # --- FK --- #
    data_wydania = models.DateField() 
    wydawnictwo = models.CharField(max_length=500)
    format = models.CharField(max_length=50, blank=True) #not required
    ilosc_stron = models.IntegerField(blank=True) #not required
    isbn = models.CharField(max_length=13, blank=True) #not required #13/10 cyfr oddzielonych -
    miejsce_wydania = models.CharField(max_length=255)
    def __str__(self):
	    return str(self.id_publikacji)+" - data wydania: "+str(self.data_wydania)+", wydawnictwo: "+str(self.wydawnictwo)+", "+str(self.format)+", "+str(self.ilosc_stron)+" str."

class Artykul(models.Model):
    id_publikacji = models.ForeignKey(Publikacja) # --- FK --- #
    data_publikacji = models.DateField() 
    czasopismo = models.CharField(max_length=500)
    zakres_stron = models.CharField(max_length=50, blank=True) #not required
    nr_czasopisma = models.CharField(max_length=50)
    def __str__(self):
	    return str(self.id_publikacji)+" - data publikacji: "+str(self.data_publikacji)+", czasopismo: "+self.czasopismo.encode('utf8')+", zakres stron: "+self.zakres_stron

class Materialy_Konferencyjne(models.Model):
    id_publikacji = models.ForeignKey(Publikacja) # --- FK --- #
    nazwa_konferencji = models.CharField(max_length=500)
    data_konferencji = models.DateField() 
    lokalizacja_konferencji = models.CharField(max_length=255)
    def __str__(self):
	    return str(self.id_publikacji)+" - nazwa konferencji: "+self.nazwa_konferencji.encode('utf8')+", data konferencji: "+str(self.data_konferencji)

class Witryna_Internetowa(models.Model):
    id_publikacji = models.ForeignKey(Publikacja) # --- FK --- #
    wlasciciel = models.CharField(max_length=255, blank=True) #not required
    adres_URL = models.CharField(max_length=255)
    data_odwiedzin = models.DateField(default=datetime.date.today) #.isoformat()
    def __str__(self):
	    return str(self.id_publikacji)+" - adres URL: "+self.adres_URL.encode('utf8')+", wlasciciel: "+self.wlasciciel.encode('utf8')+", data odwiedzin: "+str(self.data_odwiedzin)

class Rozdzial_Ksiazki(models.Model):
    id_publikacji = models.ForeignKey(Publikacja) # --- FK --- #
    id_ksiazki = models.ForeignKey(Ksiazka) # --- FK --- #
    def __str__(self):
	    return str(self.id_publikacji)+" - do ksiazki: "+str(self.id_ksiazki)

