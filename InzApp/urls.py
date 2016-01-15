from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.strona_glowna, name='strona_glowna'),
    #url(r'^/$', views.strona_glowna, name='strona_glowna'),
    url(r'^kolekcja/(?P<kolekcja_id>[0-9]+)/$', views.kolekcja, name='kolekcja'), # ?P<parametr> z views.FUNKCJA
    url(r'^publikacja/(?P<publikacja_id>[0-9]+)/$', views.publikacja, name='publikacja'),
    url(r'^moje-kolekcje/$', views.moje_kolekcje, name='moje_kolekcje'),
    url(r'^dodaj-kolekcje/$', views.dodaj_kolekcje, name='dodaj_kolekcje'),
    url(r'^dodaj-nowa-kolekcje/$', views.dodaj_nowa_kolekcje, name='dodaj_nowa_kolekcje'),
    url(r'^edytuj-kolekcje/(?P<kolekcja_id>[0-9]+)/$', views.edytuj_kolekcje, name='edytuj_kolekcje'),
    url(r'^edytuj-kolekcje-zapisz/$', views.edytuj_kolekcje_zapisz, name='edytuj_kolekcje_zapisz'),
    url(r'^usun-kolekcje/(?P<kolekcja_id>[0-9]+)/$', views.usun_kolekcje, name='usun_kolekcje'),
    url(r'^rejestracja/$', views.rejestracja, name='rejestracja'),
    url(r'^zarejestruj/$', views.zarejestruj, name='zarejestruj'),
    url(r'^logowanie/$', views.logowanie, name='logowanie'),
    url(r'^zaloguj/$', views.zaloguj, name='zaloguj'),
    url(r'^wyloguj/$', views.wyloguj, name='wyloguj'),
    url(r'^dodaj-publikacje/$', views.dodaj_publikacje, name='dodaj_publikacje'),
    url(r'^dodaj-nowa-publikacje/$', views.dodaj_nowa_publikacje, name='dodaj_nowa_publikacje'),
    url(r'^moje-publikacje/$', views.moje_publikacje, name='moje_publikacje'),
    url(r'^dodaj-publikacje-do-kolekcji/(?P<kolekcja_id>[0-9]+)/$', views.dodaj_publikacje_do_kolekcji, name='dodaj_publikacje_do_kolekcji'),
    url(r'^dodaj-nowa-publikacje-do-kolekcji/$', views.dodaj_nowa_publikacje_do_kolekcji, name='dodaj_nowa_publikacje_do_kolekcji'),
    url(r'^usun-publikacje-z-kolekcji/(?P<kolekcja_id>[0-9]+)/(?P<publikacja_id>[0-9]+)/$', views.usun_publikacje_z_kolekcji, name='usun_publikacje_z_kolekcji'),
    url(r'^dodaj-publikacje-do_kolekcji-z-publikacji/$', views.dodaj_publikacje_do_kolekcji_z_publikacji, name='dodaj_publikacje_do_kolekcji_z_publikacji'),
    url(r'^publikacje/$', views.publikacje, name='publikacje'),
    url(r'^pola-wyszukiwania/$', views.pola_wyszukiwania, name='pola_wyszukiwania'),
    url(r'^wyniki-wyszukiwania/$', views.wyniki_wyszukiwania, name='wyniki_wyszukiwania'),
    url(r'^bibliografia/(?P<kolekcja_id>[0-9]+)/(?P<typ_id>[0-9]+)/$', views.bibliografia, name='bibliografia'),
    url(r'^ustawienia/$', views.ustawienia, name='ustawienia'),
    url(r'^zmien-ustawienia-konta/$', views.zmien_ustawienia_konta, name='zmien_ustawienia_konta'),
    url(r'^wynik/$', views.wynik, name='wynik'),
    url(r'^uzytkownicy/$', views.uzytkownicy, name='uzytkownicy'),
    url(r'^zablokuj/(?P<uzytkownik_id>[0-9]+)/(?P<zablokuj>[0-9]+)/$', views.zablokuj, name='zablokuj'),
    url(r'^usun-publikacje/(?P<publikacja_id>[0-9]+)/$', views.usun_publikacje, name='usun_publikacje'),
    url(r'^edytuj-publikacje/(?P<publikacja_id>[0-9]+)/$', views.edytuj_publikacje, name='edytuj_publikacje'),
]

handler404 = 'views.page_not_found' 
