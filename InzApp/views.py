# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.db.models import F, Q
from django.template import RequestContext
from django.shortcuts import redirect
from django.utils.timesince import timesince

from django.views.defaults import page_not_found as default_page_not_found 
from django.views.defaults import server_error as default_server_error 

from InzApp.models import Kolekcja, Uzytkownik, Publikacja, Kolekcja_Publikacja, Ksiazka, Artykul, Materialy_Konferencyjne, Witryna_Internetowa, Rozdzial_Ksiazki, Autor, Dziedzina, Jezyk

import hashlib
import operator
import datetime
import sys
from  math import ceil

reload(sys)
sys.setdefaultencoding('utf-8')

def strona_glowna(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        zalogowany["jest_administratorem"] = Uzytkownik.objects.get(id = zalogowany["id"]).jest_administratorem
        utworzone_kolekcje = Kolekcja.objects.filter(id_uzytkownika__exact = Uzytkownik.objects.get(id = zalogowany["id"]))
        statystyka = {}
        statystyka["utworzone_kolekcje"] = utworzone_kolekcje.count()
        utworzone_publikacje = Publikacja.objects.filter(utworzyl__exact = zalogowany["login"])
        statystyka["utworzone_publikacje"] = utworzone_publikacje.count()
        liczba_ksiazek = 0
        liczba_artykulow = 0
        liczba_materialow = 0
        liczba_witryn = 0
        liczba_rozdzialow = 0
        for kolekcja in utworzone_kolekcje:
            kolekcja_publikacja = Kolekcja_Publikacja.objects.filter(id_kolekcji__exact = Kolekcja.objects.get(id = kolekcja.id))
            for kp in kolekcja_publikacja:
                liczba_ksiazek += Ksiazka.objects.filter(id_publikacji__exact = kp.id_publikacji).count()
                liczba_artykulow += Artykul.objects.filter(id_publikacji__exact = kp.id_publikacji).count()
                liczba_materialow += Materialy_Konferencyjne.objects.filter(id_publikacji__exact = kp.id_publikacji).count()
                liczba_witryn += Witryna_Internetowa.objects.filter(id_publikacji__exact = kp.id_publikacji).count()
                liczba_rozdzialow += Rozdzial_Ksiazki.objects.filter(id_publikacji__exact = kp.id_publikacji).count()
        statystyka["ksiazki"] = liczba_ksiazek
        statystyka["artykuly"] = liczba_artykulow
        statystyka["materialy"] = liczba_materialow
        statystyka["witryny"] = liczba_witryn
        statystyka["rozdzialy"] = liczba_rozdzialow
        statystyka["liczba_publikacji"] = liczba_ksiazek + liczba_artykulow + liczba_materialow + liczba_witryn + liczba_rozdzialow
        if statystyka["liczba_publikacji"] != 0:
            statystyka["ksiazki_p"] = (liczba_ksiazek * 100) / statystyka["liczba_publikacji"]
            statystyka["artykuly_p"] = (liczba_artykulow * 100) / statystyka["liczba_publikacji"]
            statystyka["materialy_p"] = (liczba_materialow * 100) / statystyka["liczba_publikacji"]
            statystyka["witryny_p"] = (liczba_witryn * 100) / statystyka["liczba_publikacji"]
            statystyka["rozdzialy_p"] = (liczba_rozdzialow * 100) / statystyka["liczba_publikacji"]
        else:
            statystyka["ksiazki_p"] = 0
            statystyka["artykuly_p"] = 0
            statystyka["materialy_p"] = 0
            statystyka["witryny_p"] = 0
            statystyka["rozdzialy_p"] = 0
        kontekst = {
            'zalogowany': zalogowany,
            'statystyka': statystyka,
        }
        return render(request, 'InzApp/index.html', kontekst)

def kolekcja(request, kolekcja_id):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {}
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        obiekt = Kolekcja.objects.filter(id = kolekcja_id)
        if obiekt.count() > 0:
            k = Kolekcja.objects.get(id = kolekcja_id)
            if k.id_uzytkownika.id != zalogowany["id"]:
                if k.czy_publiczna == False:
                    wynik = {}
                    wynik["nazwa"] = 'Brak dostępu!'
                    wynik["opis"] = 'Prywatna kolekcja!'
                    wynik["nazwa_podstrony"] = 'Brak dostępu'
                    wynik["url_przekierowania"] = 'kolekcje'
                    kontekst = {
                        'wynik': wynik,		
                    }
                    return render(request, 'InzApp/wynik.html', kontekst)
            moje_kolekcje = Kolekcja.objects.filter(id_uzytkownika__exact = Uzytkownik.objects.get(id = zalogowany["id"])).exclude(id = kolekcja_id)
            kontekst = {
                'nazwa': k.nazwa_kolekcji,
                'opis': k.opis,
                'data_utworzenia': str(k.data_utworzenia),
                'data_modyfikacji': str(k.data_modyfikacji),
                'uzytkownik': k.id_uzytkownika,
                'czy_publiczna': k.czy_publiczna, 
                'kp': Kolekcja_Publikacja.objects.filter(id_kolekcji__exact = k),
                'zalogowany': zalogowany,
                'kolekcja': k.id, 
                'moje_kolekcje': moje_kolekcje,
            }
            return render(request, 'InzApp/kolekcja.html', kontekst)
        else:
            wynik = {}
            wynik["nazwa"] = 'Błąd!'
            wynik["opis"] = 'Nie ma takiej kolekcji!'
            wynik["nazwa_podstrony"] = 'Błąd'
            wynik["url_przekierowania"] = 'kolekcje'
            kontekst = {
                'wynik': wynik,		
            }
            return render(request, 'InzApp/wynik.html', kontekst)

def publikacja(request, publikacja_id):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {}
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        obiekt = Publikacja.objects.filter(id = publikacja_id)
        if obiekt.count() > 0:
            p = Publikacja.objects.get(id = publikacja_id)
            if p.czy_publiczna == False:
                wynik = {}
                wynik["nazwa"] = 'Brak dostępu!'
                wynik["opis"] = 'Kolekcja prywatna! Brak dostępu.'
                wynik["nazwa_podstrony"] = 'Brak dostępu'
                wynik["url_przekierowania"] = 'strona_glowna'
                kontekst = {
                    'wynik': wynik,		
                }
                return render(request, 'InzApp/wynik.html', kontekst)
            if p.rodzaj == 'K':
                o_publikacji = Ksiazka.objects.get(id_publikacji__exact = p)
            elif p.rodzaj == 'A':
                o_publikacji = Artykul.objects.get(id_publikacji__exact = p)
            elif p.rodzaj == 'M':
                o_publikacji = Materialy_Konferencyjne.objects.get(id_publikacji__exact = p)
            elif p.rodzaj == 'W':
                o_publikacji = Witryna_Internetowa.objects.get(id_publikacji__exact = p)
            elif p.rodzaj == 'R':
                o_publikacji = Rozdzial_Ksiazki.objects.get(id_publikacji__exact = p)
            kp = Kolekcja_Publikacja.objects.filter(id_publikacji__exact = Publikacja.objects.get(id = publikacja_id)).values("id_kolekcji") #wartosci danego pola z QuerySet !!!
            kolekcje_w_ktorych_juz_jest = []
            kolekcje = Kolekcja.objects.filter(id_uzytkownika__exact = Uzytkownik.objects.get(id = zalogowany["id"])).exclude(id__in = kp)
            kontekst = {
                'id': p.id, 
                'tytul': p.tytul, 
                'autor': p.autor, 
                'rodzaj_skrot': p.rodzaj,
                'rodzaj': p.get_rodzaj_display(), 
                'dziedzina': p.dziedzina.nazwa,
                'dziedzina_skrot': p.dziedzina.skrot,			
                'slowa_kluczowe': p.slowa_kluczowe, 
                'jezyk': p.jezyk.nazwa,
                'jezyk_skrot': p.jezyk.skrot,			
                'opis': p.opis, 
                'url': p.url,
                'plik': p.plik,
                'czy_publiczna': p.czy_publiczna,
                'utworzyl': p.utworzyl, #login
                'zmodyfikowal': p.zmodyfikowal, #Uzytkownik
                'data_utworzenia': str(p.data_utworzenia),
                'data_modyfikacji': str(p.data_modyfikacji),
                'o_publikacji': o_publikacji,
                'zalogowany': zalogowany,
                'kolekcje': kolekcje,
            }
            return render(request, 'InzApp/publikacja.html', kontekst) 
        else:
            wynik = {}
            wynik["nazwa"] = 'Błąd!'
            wynik["opis"] = 'Nie ma takiej publikacji!'
            wynik["nazwa_podstrony"] = 'Błąd'
            wynik["url_przekierowania"] = 'strona_glowna'
            kontekst = {
                'wynik': wynik,		
            }
            return render(request, 'InzApp/wynik.html', kontekst)
    
def moje_kolekcje(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        uzytkownik = Uzytkownik.objects.get(id = int(zalogowany["id"]))
        kolekcje = Kolekcja.objects.filter(id_uzytkownika__exact = uzytkownik)
        kontekst = {
            'zalogowany': zalogowany,
            'uzytkownik': uzytkownik,
            'kolekcje': kolekcje,
        }
        return render(request, 'InzApp/moje_kolekcje.html', kontekst)

@csrf_protect
def dodaj_kolekcje(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        kontekst = {
            'zalogowany': zalogowany,
        }
        return render(request, 'InzApp/dodaj_kolekcje.html', kontekst)

def dodaj_nowa_kolekcje(request):
    if request.POST.get('nowa_kolekcja_czy_publiczna') is None:
        publiczna = False
    else:
        publiczna = request.POST.get('nowa_kolekcja_czy_publiczna')
    uzytkownik_kolekcji = Uzytkownik.objects.get(id = request.POST.get('nowa_kolekcja_id_uzytkownika'))
    nowa_kolekcja = Kolekcja(nazwa_kolekcji = request.POST.get('nowa_kolekcja_nazwa'), opis = request.POST.get('nowa_kolekcja_opis'), data_utworzenia = timezone.now(), data_modyfikacji = timezone.now(), id_uzytkownika = uzytkownik_kolekcji, czy_publiczna = publiczna)
    nowa_kolekcja.save()
    return redirect('/moje-kolekcje') 

def edytuj_kolekcje(request, kolekcja_id):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        osoba = Uzytkownik.objects.get(id = zalogowany["id"])
        obiekt = Kolekcja.objects.filter(id = kolekcja_id)
        if obiekt.count() > 0:
            k = Kolekcja.objects.get(id = kolekcja_id)
            if k.id_uzytkownika != osoba:
                wynik = {}
                wynik["nazwa"] = 'Brak dostępu!'
                wynik["opis"] = 'Prywatna kolekcja! Brak uprawnień do edycji!'
                wynik["nazwa_podstrony"] = 'Brak dostępu'
                wynik["url_przekierowania"] = 'kolekcje'
                kontekst = {
                    'wynik': wynik,		
                }
                return render(request, 'InzApp/wynik.html', kontekst)
            kontekst = {
                'kolekcja': k,
                'zalogowany': zalogowany,
            }
            return render(request, 'InzApp/edytuj_kolekcje.html', kontekst)
        else:
            wynik = {}
            wynik["nazwa"] = 'Błąd!'
            wynik["opis"] = 'Nie ma takiej kolekcji!'
            wynik["nazwa_podstrony"] = 'Błąd'
            wynik["url_przekierowania"] = 'kolekcje'
            kontekst = {
                'wynik': wynik,		
            }
            return render(request, 'InzApp/wynik.html', kontekst)

def edytuj_kolekcje_zapisz(request):
    uzytkownik = Uzytkownik.objects.get(id = request.POST.get('edytuj_kolekcje_id_uzytkownika'))
    kolekcja = Kolekcja.objects.get(id = request.POST.get('edytuj_kolekcje_id'))
    if kolekcja.id_uzytkownika == uzytkownik:
        kolekcja.nazwa_kolekcji = request.POST.get('edytuj_kolekcje_nazwa')
        kolekcja.opis = request.POST.get('edytuj_kolekcje_opis')
        kolekcja.data_modyfikacji = timezone.now()
        if request.POST.get('edytuj_kolekcje_czy_publiczna') is None: #==null
            kolekcja.czy_publiczna = False
        else:
            kolekcja.czy_publiczna = request.POST.get('edytuj_kolekcje_czy_publiczna')
        kolekcja.save()
        return redirect('/moje-kolekcje') 
    else:
        wynik = {}
        wynik["nazwa"] = 'Błąd!'
        wynik["opis"] = 'Brak możliwości edycji tej kolekcji!'
        wynik["nazwa_podstrony"] = 'Błąd'
        wynik["url_przekierowania"] = 'kolekcje'
        kontekst = {
            'wynik': wynik,		
        }
        return render(request, 'InzApp/wynik.html', kontekst)

def usun_kolekcje(request, kolekcja_id):
    kolekcja = Kolekcja.objects.get(id = kolekcja_id)
    kolekcja.delete()
    return redirect('/moje-kolekcje') 

def rejestracja(request):
    return render(request, 'InzApp/rejestracja.html')

def zarejestruj(request):
    nowy = Uzytkownik(login = request.POST.get('rejestracja_login'), haslo = hashlib.sha1(request.POST.get('rejestracja_haslo')).hexdigest(), email = request.POST.get('rejestracja_email'), data_ostatniego_logowania = timezone.now()) 
    nowy.save()
    return redirect('/') 

def logowanie(request):
    return render(request, 'InzApp/logowanie.html')

def zaloguj(request):
    login = request.POST.get('logowanie_login')
    haslo = request.POST.get('logowanie_haslo')
    uzytkownicy = Uzytkownik.objects.filter(login__exact = login)
    if uzytkownicy.count() > 0:
        uzytkownik = Uzytkownik.objects.get(login__exact = login)
        kontekst = { 'zalogowany': uzytkownik }
        haslo_hash = hashlib.sha1(haslo).hexdigest()
        if haslo_hash == uzytkownik.haslo:
            request.session["zalogowany_id"] = uzytkownik.id
            request.session["zalogowany_login"] = uzytkownik.login
            request.session["zalogowany_email"] = uzytkownik.email
            request.session["zalogowany_ostatnio"] = str(uzytkownik.data_ostatniego_logowania)
            c = RequestContext(request, {
                'foo': 'bar',
            })
            if uzytkownik.zablokowany == True:
                wynik = {}
                wynik["nazwa"] = 'Użytkownik zablokowany!'
                wynik["opis"] = 'Odmowa zalogowania się użytkownika do portalu Thesis z powodu blokady przez administratora.'
                wynik["nazwa_podstrony"] = 'Użytkownik zablokowany'
                wynik["url_przekierowania"] = 'logowanie'
                kontekst = {
                    'wynik': wynik,		
                }
                return render(request, 'InzApp/wynik.html', kontekst)
            wynik = {}
            wynik["nazwa"] = 'Logowanie'
            wynik["opis"] = 'Trwa logowanie użytkownika do portalu Thesis.'
            wynik["nazwa_podstrony"] = 'Logowanie'
            wynik["url_przekierowania"] = 'strona_glowna'
            kontekst = {
                'wynik': wynik,		
            }
            return render(request, 'InzApp/wynik.html', kontekst)
        else:
            wynik = {}
            wynik["nazwa"] = 'Błąd logowania!'
            wynik["opis"] = 'Błędny login i/lub hasło!'
            wynik["nazwa_podstrony"] = 'Błąd'
            wynik["url_przekierowania"] = 'logowanie'
            kontekst = {
                'wynik': wynik,		
            }
            return render(request, 'InzApp/wynik.html', kontekst)
    else:
        wynik = {}
        wynik["nazwa"] = 'Błąd logowania!'
        wynik["opis"] = 'Błędny login i/lub hasło!'
        wynik["nazwa_podstrony"] = 'Błąd'
        wynik["url_przekierowania"] = 'logowanie'
        kontekst = {
            'wynik': wynik,		
        }
        return render(request, 'InzApp/wynik.html', kontekst)

def wyloguj(request):
    try:
        uzytkownik = Uzytkownik.objects.get(id = request.session["zalogowany_id"])
        uzytkownik.data_ostatniego_logowania = timezone.now()
        uzytkownik.save()
        del request.session["zalogowany_id"]
        del request.session["zalogowany_login"]
        del request.session["zalogowany_email"]
        del request.session["zalogowany_ostatnio"]
    except KeyError:
        pass
    wynik = {}
    wynik["nazwa"] = 'Wylogowywanie'
    wynik["opis"] = 'Trwa wylogowywanie użytkownika z portalu Thesis.'
    wynik["nazwa_podstrony"] = 'Wylogowywanie'
    wynik["url_przekierowania"] = 'logowanie'
    kontekst = {
        'wynik': wynik,		
    }
    return render(request, 'InzApp/wynik.html', kontekst)

def dodaj_publikacje(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        autorzy = Autor.objects.all()
        dziedziny = Dziedzina.objects.all()
        jezyki = Jezyk.objects.all()
        rodzaje = Publikacja.RODZAJE
        ksiazki = Publikacja.objects.filter(rodzaj__exact = 'K')
        kontekst = {
            'zalogowany': zalogowany,
            'autorzy': autorzy,
            'dziedziny': dziedziny,
            'jezyki': jezyki, 
            'rodzaje': rodzaje,
            'ksiazki': ksiazki,			
        }
        return render(request, 'InzApp/dodaj_publikacje.html', kontekst)

def dodaj_nowa_publikacje(request):
    if request.POST.get("nowa_publikacja_czy_publiczna") == None:
        publiczna = False
    else:
        publiczna = True
    nowa_publikacja = Publikacja(tytul = request.POST.get("nowa_publikacja_tytul"), 
    autor = Autor.objects.get(id = request.POST.get("dodaj_publikacje_autor")), 
    rodzaj = request.POST.get("dodaj_publikacje_rodzaj"), 
    dziedzina = Dziedzina.objects.get(id = request.POST.get("dodaj_publikacje_dziedzina")), 
    jezyk = Jezyk.objects.get(id = request.POST.get("dodaj_publikacje_jezyk")), 
    opis = request.POST.get("nowa_publikacja_opis"), 
    slowa_kluczowe = request.POST.get("nowa_publikacja_slowa_kluczowe"), 
    czy_publiczna = publiczna, 
    url = request.POST.get("nowa_publikacja_url"), 
    plik = request.FILES.get("nowa_publikacja_plik"), 
    utworzyl = request.POST.get("nowa_publikacja_utworzyl"), 
    zmodyfikowal = Uzytkownik.objects.get(id = request.POST.get("nowa_publikacja_zmodyfikowal")))
    nowa_publikacja.save()
    rodzaj = request.POST.get("dodaj_publikacje_rodzaj") #select name!
    if rodzaj == 'K':
        nowa_ksiazka = Ksiazka(id_publikacji = Publikacja.objects.get(id = nowa_publikacja.id),
        wydawnictwo = request.POST.get("nowa_publikacja_wydawnictwo"), 
        miejsce_wydania = request.POST.get("nowa_publikacja_miejsce_wydania"), 
        data_wydania = request.POST.get("nowa_publikacja_data_wydania"))
        if request.POST.get("nowa_publikacja_format") != '':
            nowa_ksiazka.format = request.POST.get("nowa_publikacja_format")
        if request.POST.get("nowa_publikacja_ilosc_stron") != '':
            nowa_ksiazka.ilosc_stron = request.POST.get("nowa_publikacja_ilosc_stron")
        if request.POST.get("nowa_publikacja_isbn") != '':
            nowa_ksiazka.isbn = request.POST.get("nowa_publikacja_isbn")
        nowa_ksiazka.save()
    elif rodzaj == 'A':
        nowy_artykul = Artykul(id_publikacji = Publikacja.objects.get(id = nowa_publikacja.id), 
        data_publikacji = request.POST.get("nowa_publikacja_data_publikacji"), 
        czasopismo = request.POST.get("nowa_publikacja_czasopismo"), 
        nr_czasopisma = request.POST.get("nowa_publikacja_nr_czasopisma")) 
        if request.POST.get("nowa_publikacja_zakres_stron") != '':
            nowy_artykul.zakres_stron = request.POST.get("nowa_publikacja_zakres_stron")
        nowy_artykul.save()
    elif rodzaj == 'M':
        nowe_mk = Materialy_Konferencyjne(id_publikacji = Publikacja.objects.get(id = nowa_publikacja.id), 
        nazwa_konferencji = request.POST.get("nowa_publikacja_nazwa_konferencji"), 
        data_konferencji = request.POST.get("nowa_publikacja_data_konferencji"), 
        lokalizacja_konferencji = request.POST.get("nowa_publikacja_lokalizacja_konferencji"))
        nowe_mk.save()
    elif rodzaj == 'W':
        nowa_wi = Witryna_Internetowa(id_publikacji = Publikacja.objects.get(id = nowa_publikacja.id),  
        adres_URL = request.POST.get("nowa_publikacja_adres_url"), 
        data_odwiedzin = request.POST.get("nowa_publikacja_data_odwiedzin"))
        if request.POST.get("nowa_publikacja_wlasciciel") != '':
            nowa_wi.wlasciciel = request.POST.get("nowa_publikacja_wlasciciel")
        nowa_wi.save()
    elif rodzaj == 'R':
        nowy_rk = Rozdzial_Ksiazki(id_publikacji = Publikacja.objects.get(id = nowa_publikacja.id), 
        id_ksiazki = Ksiazka.objects.get(id = request.POST.get("nowa_publikacja_id_ksiazki")))
        nowy_rk.save()
    return redirect('/moje-publikacje') #"Pomyslnie dodano publikacje."

def edytuj_publikacje_zapisz(request):
    publikacja = Publikacja.objects.get(id = request.POST.get('edytuj_publikacje_id'))
    publikacja.tytul = request.POST.get("edytuj_publikacje_tytul")
    publikacja.autor = Autor.objects.get(id = request.POST.get("edytuj_publikacje_select2_autor")) 
    publikacja.dziedzina = Dziedzina.objects.get(id = request.POST.get("edytuj_publikacje_select2_dziedzina"))
    publikacja.jezyk = Jezyk.objects.get(id = request.POST.get("edytuj_publikacje_select2_jezyk"))
    publikacja.opis = request.POST.get("edytuj_publikacje_opis")
    publikacja.slowa_kluczowe = request.POST.get("edytuj_publikacje_slowa_kluczowe")
    publikacja.czy_publiczna = request.POST.get("edytuj_publikacje_czy_publiczna")
    publikacja.url = request.POST.get("edytuj_publikacje_url")
    publikacja.plik = request.FILES.get("edytuj_publikacje_plik")
    publikacja.save()
    rodzaj = publikacja.rodzaj
    if rodzaj == 'K':
        ksiazka = Ksiazka.objects.get(id_publikacji = Publikacja.objects.get(id = publikacja.id)) 
        ksiazka.data_wydania = request.POST.get("edytuj_publikacje_data_wydania")
        ksiazka.wydawnictwo = request.POST.get("edytuj_publikacje_wydawnictwo") 
        ksiazka.format = request.POST.get("edytuj_publikacje_format")
        ksiazka.ilosc_stron = request.POST.get("edytuj_publikacje_ilosc_stron")
        ksiazka.isbn = request.POST.get("edytuj_publikacje_isbn")
        ksiazka.miejsce_wydania = request.POST.get("edytuj_publikacje_miejsce_wydania")
        ksiazka.save()
    elif rodzaj == 'A':
        artykul = Artykul.objects.get(id_publikacji = Publikacja.objects.get(id = publikacja.id))
        artykul.data_publikacji = request.POST.get("edytuj_publikacje_data_publikacji") 
        artykul.czasopismo = request.POST.get("edytuj_publikacje_czasopismo")
        artykul.zakres_stron = request.POST.get("edytuj_publikacje_zakres_stron")
        artykul.nr_czasopisma = request.POST.get("edytuj_publikacje_nr_czasopisma")
        artykul.save()
    elif rodzaj == 'M':
        mk = Materialy_Konferencyjne.objects.get(id_publikacji = Publikacja.objects.get(id = publikacja.id))
        mk.nazwa_konferencji = request.POST.get("edytuj_publikacje_nazwa_konferencji")
        mk.data_konferencji = request.POST.get("edytuj_publikacje_data_konferencji")
        mk.lokalizacja_konferencji = request.POST.get("edytuj_publikacje_lokalizacja_konferencji")
        mk.save()
    elif rodzaj == 'W':
        wi = Witryna_Internetowa.objects.get(id_publikacji = Publikacja.objects.get(id = publikacja.id)) 
        wi.wlasciciel = request.POST.get("edytuj_publikacje_wlasciciel")
        wi.adres_URL = request.POST.get("edytuj_publikacje_adres_url")
        wi.data_odwiedzin = request.POST.get("edytuj_publikacje_data_odwiedzin")
        wi.save()
    elif rodzaj == 'R':
        rk = Rozdzial_Ksiazki.objects.get(id_publikacji = Publikacja.objects.get(id = publikacja.id)) 
        rk.id_ksiazki = Ksiazka.objects.get(id = request.POST.get("edytuj_publikacje_id_ksiazki"))
        rk.save()
    wynik = {}
    wynik["nazwa"] = 'Zapisano zmiany.'
    wynik["opis"] = 'Pomyslnie zapisano zmiany w szczegółach publikacji.'
    wynik["nazwa_podstrony"] = 'Zapisano zmiany'
    wynik["url_przekierowania"] = 'moje_publikacje'
    kontekst = {
        'wynik': wynik,		
    }
    return render(request, 'InzApp/wynik.html', kontekst)

def moje_publikacje(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        uzytkownik = Uzytkownik.objects.get(id = int(zalogowany["id"]))
        publikacje = Publikacja.objects.filter(utworzyl__exact = uzytkownik.login)
        kontekst = {
            'zalogowany': zalogowany,
            'uzytkownik': uzytkownik,
            'publikacje': publikacje,
        }
        return render(request, 'InzApp/moje_publikacje.html', kontekst)
	
def publikacje(request, strona = 1): # publiczne i zalogowanego
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        uzytkownik = Uzytkownik.objects.get(id = int(zalogowany["id"]))
        elementow_na_stronie = 3
        publikacje = Publikacja.objects.filter(Q(czy_publiczna__exact = True) | Q(utworzyl__exact = uzytkownik.login))
        ile_stron = int(ceil(float(len(publikacje))/float(elementow_na_stronie)))
        publikacje = publikacje[ (int(strona)-1)*elementow_na_stronie : (int(strona)-1)*elementow_na_stronie+elementow_na_stronie ]
        zakres_stron = range(1,ile_stron+1)
        kontekst = {
            'zalogowany': zalogowany,
            'publikacje': publikacje,
            'ile_stron': ile_stron,
            'zakres_stron': zakres_stron,
            'strona': int(strona),
        }
        return render(request, 'InzApp/publikacje.html', kontekst)

def kolekcje(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        uzytkownik = Uzytkownik.objects.get(id = int(zalogowany["id"]))
        kolekcje = Kolekcja.objects.filter(Q(czy_publiczna__exact = True) | Q(id_uzytkownika__exact = uzytkownik))
        kontekst = {
            'zalogowany': zalogowany,
            'uzytkownik': uzytkownik,
            'kolekcje': kolekcje,
        }
        return render(request, 'InzApp/kolekcje.html', kontekst)

def dodaj_publikacje_do_kolekcji(request, kolekcja_id):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        kolekcja = Kolekcja.objects.get(id = kolekcja_id)
        if kolekcja.id_uzytkownika != Uzytkownik.objects.get(id = zalogowany["id"]):
            wynik = {}
            wynik["nazwa"] = 'Błąd!'
            wynik["opis"] = 'Brak uprawnień do kolekcji, której nie jesteś twórcą.'
            wynik["nazwa_podstrony"] = 'Błąd'
            wynik["url_przekierowania"] = 'strona_glowna'
            kontekst = {
                'wynik': wynik,		
            }
            return render(request, 'InzApp/wynik.html', kontekst)
        kp = Kolekcja_Publikacja.objects.filter(id_kolekcji__exact = kolekcja)
        id_publikacji_z_kolekcji = []
        for rekord in kp:
            id_publikacji_z_kolekcji.append(rekord.id_publikacji.id)
        publikacje = Publikacja.objects.filter(
        Q(czy_publiczna__exact = True) | Q(utworzyl__iexact = zalogowany["login"]) 
        ).exclude(id__in = id_publikacji_z_kolekcji)
        kontekst = {
            'zalogowany': zalogowany,
            'kolekcja': kolekcja,
            'publikacje': publikacje, 
        }
        return render(request, 'InzApp/dodaj_publikacje_do_kolekcji.html', kontekst)

def dodaj_nowa_publikacje_do_kolekcji(request):
    uzytkownik = Uzytkownik.objects.get(id = request.POST.get('publikacja_do_kolekcji_id_uzytkownika'))
    kolekcja = Kolekcja.objects.get(id = request.POST.get('publikacja_do_kolekcji_id_kolekcji'))
    publikacja = Publikacja.objects.get(id = request.POST.get('publikacja_do_kolekcji_id_publikacji'))
    nowa_publikacja_do_kolekcji = Kolekcja_Publikacja(id_kolekcji = kolekcja, id_publikacji = publikacja)
    nowa_publikacja_do_kolekcji.save()
    return redirect('/kolekcja/'+str(request.POST.get('publikacja_do_kolekcji_id_kolekcji')))

def usun_publikacje_z_kolekcji(request, kolekcja_id, publikacja_id):
    kolekcja = Kolekcja.objects.get(id = kolekcja_id)
    publikacja = Publikacja.objects.get(id = publikacja_id)
    kp = Kolekcja_Publikacja.objects.get(id_kolekcji__exact = kolekcja, id_publikacji__exact = publikacja)
    kp.delete()
    return redirect('/kolekcja/'+kolekcja_id)

def przenies_publikacje(request, publikacja_id, kolekcja_id, kolekcja_cel = 0):
    if kolekcja_cel == 0:
        return redirect('/kolekcja/'+kolekcja_id)
    publikacja = Publikacja.objects.get(id = publikacja_id)
    kolekcja_z = Kolekcja.objects.get(id = kolekcja_id)
    kolekcja_do = Kolekcja.objects.get(id = kolekcja_cel)
    czy_istnieje = Kolekcja_Publikacja.objects.filter(id_kolekcji__exact = kolekcja_do, id_publikacji__exact = publikacja)
    if czy_istnieje.count() == 0:
        nowa_kp = Kolekcja_Publikacja(id_kolekcji = kolekcja_do, id_publikacji = publikacja)
        nowa_kp.save()
    kp = Kolekcja_Publikacja.objects.get(id_kolekcji__exact = kolekcja_z, id_publikacji__exact = publikacja)
    kp.delete()
    return redirect('/kolekcja/'+kolekcja_id)

def dodaj_publikacje_do_kolekcji_z_publikacji(request):
    nowa_kp = Kolekcja_Publikacja(id_kolekcji = Kolekcja.objects.get(id = request.POST.get('publikacja_dodaj_do_kolekcji_kolekcja')), id_publikacji = Publikacja.objects.get(id = request.POST.get('publikacja_dodaj_do_kolekcji_publikacja')))
    nowa_kp.save()
    return redirect('/publikacja/'+str(nowa_kp.id_publikacji.id))
	
def pola_wyszukiwania(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        dziedziny = Dziedzina.objects.all()
        jezyki = Jezyk.objects.all()
        rodzaje = Publikacja.RODZAJE
        kontekst = {
            'zalogowany': zalogowany, 
            'dziedziny': dziedziny,
            'jezyki': jezyki, 
            'rodzaje': rodzaje,
        }
        return render(request, 'InzApp/pola_wyszukiwania.html', kontekst)

def wyniki_wyszukiwania(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        uzytkownik = Uzytkownik.objects.get(id = int(zalogowany["id"]))
        lista_warunkow = []
        lista_warunkow.append( Q(Q(czy_publiczna__exact = True) | Q(utworzyl__exact = uzytkownik.login)) ) 
        if request.POST.get('p_tytul') != "":
            lista_warunkow.append( Q(tytul__icontains = request.POST.get('p_tytul')) )
        if request.POST.get('p_autor') != "":
            lista_warunkow.append( Q(Q(autor__imie__icontains = request.POST.get('p_autor')) | Q(autor__nazwisko__icontains = request.POST.get('p_autor'))) ) 
        if request.POST.get('p_kluczowe') != "":
            lista_warunkow.append( Q(slowa_kluczowe__icontains = request.POST.get('p_kluczowe')) )
        if request.POST.get('p_opis') != "":
            lista_warunkow.append( Q(opis__icontains = request.POST.get('p_opis')) )
        if request.POST.get('p_rodzaj') != "dowolny":
            lista_warunkow.append( Q(rodzaj__exact = request.POST.get('p_rodzaj')) ) 
        if request.POST.get('p_dziedzina') != "dowolny":
            lista_warunkow.append( Q(dziedzina__exact = Dziedzina.objects.get(id = request.POST.get('p_dziedzina'))) )
        if request.POST.get('p_jezyk') != "dowolny":
            lista_warunkow.append( Q(jezyk__exact = Jezyk.objects.get(id = request.POST.get('p_jezyk'))) )
        wyszukane_publikacje = Publikacja.objects.filter( reduce(operator.and_, lista_warunkow) )
        kontekst = {
            'zalogowany': zalogowany, 
            'wyszukane_publikacje': wyszukane_publikacje,
        }
        return render(request, 'InzApp/wyniki_wyszukiwania.html', kontekst)

def bibliografia(request, kolekcja_id, typ_id):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        kolekcja = Kolekcja.objects.get(id = kolekcja_id)
        kp = Kolekcja_Publikacja.objects.filter(id_kolekcji__exact = kolekcja).order_by('id_publikacji__autor__nazwisko', 'id_publikacji__tytul')
        bibliografia_lista = []
        for publikacja in kp:
            opis = []
            if typ_id == '1': # if harvard:
                if publikacja.id_publikacji.rodzaj == 'K':
                    szczegoly = Ksiazka.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append( publikacja.id_publikacji.autor.nazwisko + ", " + publikacja.id_publikacji.autor.imie[0] + ". (" + str(szczegoly.data_wydania.year) + "). " )
                    opis.append( publikacja.id_publikacji.tytul + "," )
                    opis.append( szczegoly.miejsce_wydania + ": " + szczegoly.wydawnictwo + "." )
                if publikacja.id_publikacji.rodzaj == 'A':
                    szczegoly = Artykul.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append( publikacja.id_publikacji.autor.nazwisko + ", " + publikacja.id_publikacji.autor.imie[0] + ". (" + str(szczegoly.data_publikacji.year) + "). " + publikacja.id_publikacji.tytul + "," )
                    opis.append( szczegoly.czasopismo + "," )
                    opis.append( szczegoly.nr_czasopisma + ", s. " + szczegoly.zakres_stron + "." )
                if publikacja.id_publikacji.rodzaj == 'M':
                    szczegoly = Materialy_Konferencyjne.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append( publikacja.id_publikacji.autor.nazwisko + ", " + publikacja.id_publikacji.autor.imie[0] + ". (" + str(szczegoly.data_konferencji.year) + "). " ) 
                    opis.append( publikacja.id_publikacji.tytul + "," )
                    opis.append( szczegoly.nazwa_konferencji + ", " + szczegoly.lokalizacja_konferencji + ".")
                if publikacja.id_publikacji.rodzaj == 'W':
                    szczegoly = Witryna_Internetowa.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append( publikacja.id_publikacji.autor.nazwisko + ", " + publikacja.id_publikacji.autor.imie[0] + ". (" + str(szczegoly.data_odwiedzin.year) + "). " )
                    opis.append( publikacja.id_publikacji.tytul + "," )
                    opis.append( "[Online]. Dostępne z: " + szczegoly.adres_URL + ". [Dostęp: " + str(szczegoly.data_odwiedzin)[0:10] + "]." )
                if publikacja.id_publikacji.rodzaj == 'R':
                    szczegoly = Rozdzial_Ksiazki.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append( publikacja.id_publikacji.autor.nazwisko + ", " + publikacja.id_publikacji.autor.imie[0] + ". (" + str(szczegoly.id_ksiazki.data_wydania.year) + "). " + publikacja.id_publikacji.tytul + ", w:" )
                    opis.append( szczegoly.id_ksiazki.id_publikacji.tytul + "," )
                    opis.append( "praca zbiorowa pod red. " + szczegoly.id_ksiazki.id_publikacji.autor.imie + " " + szczegoly.id_ksiazki.id_publikacji.autor.nazwisko + ", " + szczegoly.id_ksiazki.miejsce_wydania + ": " + szczegoly.id_ksiazki.wydawnictwo + ". " )
            if typ_id == '2': # if IEEE:
                if publikacja.id_publikacji.rodzaj == 'K':
                    szczegoly = Ksiazka.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append( publikacja.id_publikacji.autor.imie[0] + ". " + publikacja.id_publikacji.autor.nazwisko + ", " )
                    opis.append( publikacja.id_publikacji.tytul + ",") #kursywa
                    opis.append( szczegoly.miejsce_wydania + ": " + szczegoly.wydawnictwo + ", " + str(szczegoly.data_wydania.year) + "." )
                if publikacja.id_publikacji.rodzaj == 'A':
                    szczegoly = Artykul.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append( publikacja.id_publikacji.autor.imie[0] + ". " + publikacja.id_publikacji.autor.nazwisko + ", " + "'" + publikacja.id_publikacji.tytul + "', " )
                    opis.append( szczegoly.czasopismo ) #kursywa
                    opis.append( ", " + szczegoly.nr_czasopisma + ", " + str(szczegoly.data_publikacji.year) + "." )
                if publikacja.id_publikacji.rodzaj == 'M':
                    szczegoly = Materialy_Konferencyjne.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append( publikacja.id_publikacji.autor.imie[0] + ". " + publikacja.id_publikacji.autor.nazwisko + ", " + "'" + publikacja.id_publikacji.tytul + "', " )
                    opis.append( szczegoly.nazwa_konferencji + "," ) #kursywa
                    opis.append( szczegoly.lokalizacja_konferencji + ", " + str(szczegoly.data_konferencji.year) + "." )
                if publikacja.id_publikacji.rodzaj == 'W':
                    szczegoly = Witryna_Internetowa.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append( publikacja.id_publikacji.autor.imie[0] + ". " + publikacja.id_publikacji.autor.nazwisko + ", " + "'" + publikacja.id_publikacji.tytul + "', " + str(szczegoly.data_odwiedzin.year) + ". [Online]. Dostępne: " + szczegoly.adres_URL + ". [Dostęp: " + str(szczegoly.data_odwiedzin)[0:10] + "]." )
                if publikacja.id_publikacji.rodzaj == 'R':
                    szczegoly = Rozdzial_Ksiazki.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append( publikacja.id_publikacji.autor.imie[0] + ". " + publikacja.id_publikacji.autor.nazwisko + ", " + "'" + publikacja.id_publikacji.tytul + "', " + "w " )
                    opis.append( szczegoly.id_ksiazki.id_publikacji.tytul + "," ) #kursywa
                    opis.append( szczegoly.id_ksiazki.miejsce_wydania + ": " + szczegoly.id_ksiazki.wydawnictwo + ", " + str(szczegoly.id_ksiazki.data_wydania.year) + "." )
            if typ_id == '3': # if bibtex
                klucz_cytowania = kolekcja.id_uzytkownika.login+'-'+str(kolekcja.id)
                if publikacja.id_publikacji.rodzaj == 'K':
                    szczegoly = Ksiazka.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append('@Book{'+klucz_cytowania+', author = "'+publikacja.id_publikacji.autor.imie+' '+publikacja.id_publikacji.autor.nazwisko+'", title = "'+publikacja.id_publikacji.tytul+'", publisher = "'+szczegoly.wydawnictwo+'", year = "'+str(szczegoly.data_wydania.year)+'", isbn = "'+szczegoly.isbn+'"}')
                if publikacja.id_publikacji.rodzaj == 'A':
                    szczegoly = Artykul.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append('@Article{'+klucz_cytowania+', author = "'+publikacja.id_publikacji.autor.imie+' '+publikacja.id_publikacji.autor.nazwisko+'", title = "'+publikacja.id_publikacji.tytul+'", journal = "'+szczegoly.czasopismo+'", year = "'+str(szczegoly.data_publikacji.year)+'", pages = "'+szczegoly.zakres_stron+'"}')
                if publikacja.id_publikacji.rodzaj == 'M':
                    szczegoly = Materialy_Konferencyjne.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append('@Inproceedings{'+klucz_cytowania+', author = "'+publikacja.id_publikacji.autor.imie+' '+publikacja.id_publikacji.autor.nazwisko+'", title = "'+publikacja.id_publikacji.tytul+'", booktitle = "'+szczegoly.nazwa_konferencji+'", year = "'+str(szczegoly.data_konferencji.year)+'"}')
                if publikacja.id_publikacji.rodzaj == 'W':
                    szczegoly = Witryna_Internetowa.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append('@misc{'+klucz_cytowania+', author = "'+publikacja.id_publikacji.autor.imie+' '+publikacja.id_publikacji.autor.nazwisko+'", title = "'+publikacja.id_publikacji.tytul+'", howpublished = "[Online]", year = "'+str(szczegoly.data_odwiedzin.year)+'", note = "[Dostęp: '+str(szczegoly.data_odwiedzin)[0:10]+']", annote = "Dostępny w Internecie: \url{'+szczegoly.adres_URL+'}" }')
                if publikacja.id_publikacji.rodzaj == 'R':
                    szczegoly = Rozdzial_Ksiazki.objects.get(id_publikacji__exact = publikacja.id_publikacji.id)
                    opis.append('@Incollection{'+klucz_cytowania+', author = "'+publikacja.id_publikacji.autor.imie+' '+publikacja.id_publikacji.autor.nazwisko+'", title = "'+publikacja.id_publikacji.tytul+'", booktitle = "'+szczegoly.id_ksiazki.id_publikacji.tytul+'", publisher = "'+szczegoly.id_ksiazki.wydawnictwo+'", year = "'+str(szczegoly.id_ksiazki.data_wydania.year)+'}')
            bibliografia_lista.append(opis)
        kontekst = {
            'zalogowany': zalogowany, 
            'bibliografia_lista': bibliografia_lista,
            'typ': typ_id,			
        }
        return render(request, 'InzApp/bibliografia.html', kontekst)

def ustawienia(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        zalogowany_uzytkownik = Uzytkownik.objects.get(id = request.session["zalogowany_id"])
        kontekst = {
            'zalogowany': zalogowany, 
            'email': zalogowany_uzytkownik.email,			
        }
        return render(request, 'InzApp/ustawienia.html', kontekst)

def zmien_ustawienia_konta(request):
    zalogowany = Uzytkownik.objects.get(id = request.POST.get('ustawienia_id_uzytkownika'))
    if hashlib.sha1(request.POST.get('ustawienia_bhaslo')).hexdigest() == zalogowany.haslo:
        if request.POST.get('ustawienia_nhaslo') == request.POST.get('ustawienia_pnhaslo'):
            if request.POST.get('ustawienia_nhaslo') != "":
                zalogowany.haslo = hashlib.sha1(request.POST.get('ustawienia_nhaslo')).hexdigest()
        zalogowany.email = request.POST.get('ustawienia_email')
        zalogowany.data_modyfikacji = datetime.datetime.now()
        zalogowany.save()
        return redirect('/ustawienia') #"Zapisano zmiany."
    else:
        wynik = {}
        wynik["nazwa"] = 'Błąd!'
        wynik["opis"] = 'Błędne bieżące hasło.'
        wynik["nazwa_podstrony"] = 'Błąd'
        wynik["url_przekierowania"] = 'ustawienia'
        kontekst = {
            'wynik': wynik,		
        }
        return render(request, 'InzApp/wynik.html', kontekst)

def wynik(request):
    wynik = {}
    wynik["nazwa"] = 'Błąd!'
    wynik["opis"] = 'Dłuższy tekst opisujący co się stało. Uważaj, by coś tam. Zaraz Cię przekieruje gdzieś tam. Dziękujęmy.'
    wynik["nazwa_podstrony"] = 'Strona z błędem'
    wynik["url_przekierowania"] = 'strona_glowna'
    kontekst = {
        'wynik': wynik,		
    }
    return render(request, 'InzApp/wynik.html', kontekst)

def uzytkownicy(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        zalogowany_uzytkownik = Uzytkownik.objects.get(id = request.session["zalogowany_id"])
        if zalogowany_uzytkownik.jest_administratorem == True:
            lista_uzytkownikow = Uzytkownik.objects.all()
            kontekst = {
                'zalogowany': zalogowany, 
                'lista_uzytkownikow': lista_uzytkownikow,			
            }
            return render(request, 'InzApp/uzytkownicy.html', kontekst)
        else:
            wynik = {}
            wynik["nazwa"] = 'Brak dostępu!'
            wynik["opis"] = 'Ta podstrona dostępna jest tylko dla administratora.'
            wynik["nazwa_podstrony"] = 'Brak dostępu'
            wynik["url_przekierowania"] = 'strona_glowna'
            kontekst = {
                'wynik': wynik,		
            }
            return render(request, 'InzApp/wynik.html', kontekst)

def zablokuj(request, uzytkownik_id, zablokuj):
    uzytkownik = Uzytkownik.objects.get(id = uzytkownik_id)
    if zablokuj == '1':
        uzytkownik.zablokowany = True
    else:
        uzytkownik.zablokowany = False
    uzytkownik.save()
    wynik = {}
    wynik["nazwa"] = 'Zapisano zmiany.'
    wynik["opis"] = 'Pomyślnie zapisano zmiany w koncie użytkownika. Za chwilę będziesz mógł edytować szczegóły innych użytkowników aplikacji.'
    wynik["nazwa_podstrony"] = 'Zapisano zamiany'
    wynik["url_przekierowania"] = 'uzytkownicy'
    kontekst = {
        'wynik': wynik,		
    }
    return render(request, 'InzApp/wynik.html', kontekst)

def usun_publikacje(request, publikacja_id):
    publikacja = Publikacja.objects.get(id = publikacja_id)
    if publikacja.rodzaj == 'K':
        powiazane = Ksiazka.objects.get(id_publikacji__exact = publikacja_id)
    if publikacja.rodzaj == 'A':
        powiazane = Artykul.objects.get(id_publikacji__exact = publikacja_id)
    if publikacja.rodzaj == 'M':
        powiazane = Materialy_Konferencyjne.objects.get(id_publikacji__exact = publikacja_id)
    if publikacja.rodzaj == 'W':
        powiazane = Witryna_Internetowa.objects.get(id_publikacji__exact = publikacja_id)
    if publikacja.rodzaj == 'R':
        powiazane = Rozdzial_Ksiazki.objects.get(id_publikacji__exact = publikacja_id)
    powiazane.delete()
    kp = Kolekcja_Publikacja.objects.filter(id_publikacji__exact = publikacja_id)
    kp.delete()
    publikacja.delete()
    wynik = {}
    wynik["nazwa"] = 'Usunięto publikację.'
    wynik["opis"] = 'Pomyślnie usunięto publikację z bazy danych aplikacji.'
    wynik["nazwa_podstrony"] = 'Usunięto publikację'
    wynik["url_przekierowania"] = 'moje_publikacje'
    kontekst = {
        'wynik': wynik,		
    }
    return render(request, 'InzApp/wynik.html', kontekst)

def page_not_found(request, template_name='InzApp/404.html'): 
    return default_page_not_found(request, template_name=template_name)

def edytuj_publikacje(request, publikacja_id):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {}
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        obiekt = Publikacja.objects.filter(id = publikacja_id)
        if obiekt.count() > 0:
            p = Publikacja.objects.get(id = publikacja_id)
            if p.utworzyl != zalogowany["login"]:
                wynik = {}
                wynik["nazwa"] = 'Brak dostępu!'
                wynik["opis"] = 'Brak uprawnień do edycji tej publikacji!'
                wynik["nazwa_podstrony"] = 'Brak dostępu'
                wynik["url_przekierowania"] = 'strona_glowna'
                kontekst = {
                    'wynik': wynik,		
                }
                return render(request, 'InzApp/wynik.html', kontekst)
            if p.rodzaj == 'K':
                o_publikacji = Ksiazka.objects.get(id_publikacji__exact = p)
            elif p.rodzaj == 'A':
                o_publikacji = Artykul.objects.get(id_publikacji__exact = p)
            elif p.rodzaj == 'M':
                o_publikacji = Materialy_Konferencyjne.objects.get(id_publikacji__exact = p)
            elif p.rodzaj == 'W':
                o_publikacji = Witryna_Internetowa.objects.get(id_publikacji__exact = p)
            elif p.rodzaj == 'R':
                o_publikacji = Rozdzial_Ksiazki.objects.get(id_publikacji__exact = p)
            autorzy = Autor.objects.all()
            dziedziny = Dziedzina.objects.all()
            jezyki = Jezyk.objects.all()
            ksiazki = Publikacja.objects.filter(rodzaj__exact = 'K')
            kontekst = {
                'zalogowany': zalogowany,
                'publikacja': p,
                'o_publikacji': o_publikacji,
                'autorzy': autorzy,
                'dziedziny': dziedziny,
                'jezyki': jezyki, 
                'ksiazki': ksiazki,
            }
            return render(request, 'InzApp/edytuj_publikacje.html', kontekst) 
        else:
            wynik = {}
            wynik["nazwa"] = 'Błąd!'
            wynik["opis"] = 'Nie ma takiej publikacji!'
            wynik["nazwa_podstrony"] = 'Błąd'
            wynik["url_przekierowania"] = 'strona_glowna'
            kontekst = {
                'wynik': wynik,		
            }
            return render(request, 'InzApp/wynik.html', kontekst)

def dodaj_autora(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        kontekst = {
            'zalogowany': zalogowany,
        }
        return render(request, 'InzApp/dodaj_autora.html', kontekst)

def dodaj_nowego_autora(request):
    opis_autora = request.POST.get('nowy_autor_opis')
    if opis_autora != '':
        autor = Autor(imie = request.POST.get('nowy_autor_imie'), nazwisko = request.POST.get('nowy_autor_nazwisko'), opis = opis_autora)
    else:
        autor = Autor(imie = request.POST.get('nowy_autor_imie'), nazwisko = request.POST.get('nowy_autor_nazwisko'))
    autor.save()
    wynik = {}
    wynik["nazwa"] = 'Dodano autora.'
    wynik["opis"] = 'Pomyślnie dodano nowego autora do bazy danych aplikacji.'
    wynik["nazwa_podstrony"] = 'Dodano autora'
    wynik["url_przekierowania"] = 'dodaj_autora'
    kontekst = {
        'wynik': wynik,		
    }
    return render(request, 'InzApp/wynik.html', kontekst)

def edytuj_autora(request, autor_id):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        autor = Autor.objects.get(id = autor_id)
        kontekst = {
            'zalogowany': zalogowany,
            'autor': autor,
        }
        return render(request, 'InzApp/edytuj_autora.html', kontekst)

def edytuj_autora_zapisz(request):
    autor = Autor.objects.get(id = request.POST.get('edytuj_autor_id'))
    autor.imie = request.POST.get('edytuj_autor_imie')
    autor.nazwisko = request.POST.get('edytuj_autor_nazwisko')
    autor.opis = request.POST.get('edytuj_autor_opis')
    autor.save()
    wynik = {}
    wynik["nazwa"] = 'Zapisano zmiany.'
    wynik["opis"] = 'Pomyślnie zapisano zmiany w danych autora.'
    wynik["nazwa_podstrony"] = 'Zapisano zmiany'
    wynik["url_przekierowania"] = 'strona_glowna'
    kontekst = {
        'wynik': wynik,		
    }
    return render(request, 'InzApp/wynik.html', kontekst)

def autorzy(request):
    if "zalogowany_login" not in request.session:
        return logowanie(request) #gdy niezalogowany
    else:
        zalogowany = {} # = [] gdy liczby jako klucze
        zalogowany["login"] = request.session["zalogowany_login"]
        zalogowany["id"] = request.session["zalogowany_id"]
        zalogowany["email"] = request.session["zalogowany_email"]
        zalogowany["ostatnio"] = request.session["zalogowany_ostatnio"]
        autorzy = Autor.objects.all()
        kontekst = {
            'zalogowany': zalogowany,
            'autorzy': autorzy,
        }
        return render(request, 'InzApp/autorzy.html', kontekst)