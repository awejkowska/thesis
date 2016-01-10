from django.contrib import admin

# Register your models here.

from .models import Uzytkownik, Kolekcja, Publikacja, Kolekcja_Publikacja, Autor, Ksiazka, Artykul, Materialy_Konferencyjne, Witryna_Internetowa, Rozdzial_Ksiazki, Jezyk, Dziedzina

admin.site.register(Uzytkownik)
admin.site.register(Kolekcja)
admin.site.register(Publikacja)
admin.site.register(Kolekcja_Publikacja)
admin.site.register(Autor)
admin.site.register(Ksiazka)
admin.site.register(Artykul)
admin.site.register(Materialy_Konferencyjne)
admin.site.register(Witryna_Internetowa)
admin.site.register(Rozdzial_Ksiazki)
admin.site.register(Jezyk)
admin.site.register(Dziedzina)