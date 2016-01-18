function sprawdz_email(email) 
{
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
}

function rejestracja_sprawdz()
{
	var login = document.getElementById("rejestracja_login").value;
	var haslo = document.getElementById("rejestracja_haslo").value;
	var haslo_powtorz = document.getElementById("rejestracja_haslo_powtorz").value;
	var email = document.getElementById("rejestracja_email").value;
	
	if (login == "" || haslo == "" || haslo_powtorz == "" || email == "" ||
	 login == null || haslo == null || haslo_powtorz == null || email == null)
	{
		alert("Uzupełnij wszystkie pola!");
		return false;
	}
	else 
	{
		if (sprawdz_email(email) == false)
		{
			alert("Niepoprawny format e-mail!");
			return false;
		}
		else if (haslo != haslo_powtorz)
		{
			alert("Podane hasła różnią się!");
			return false;
		}
		else if (haslo.length < 6)
		{
			alert("Podane hasło jest za krótkie (minimum 6 znaków)!");
			return false;
		}
		else 
		{
			return true;
		}
	}
}

function ustaw_pola_formularza_dodawania_publikacji_wg_rodzaju() 
{
	ukryj_pola_formularza_dodawania_publikacji_wg_rodzaju("dodaj_publikacje_ksiazka");
	ukryj_pola_formularza_dodawania_publikacji_wg_rodzaju("dodaj_publikacje_artykul");
	ukryj_pola_formularza_dodawania_publikacji_wg_rodzaju("dodaj_publikacje_materialy");
	ukryj_pola_formularza_dodawania_publikacji_wg_rodzaju("dodaj_publikacje_witryna");
	ukryj_pola_formularza_dodawania_publikacji_wg_rodzaju("dodaj_publikacje_rozdzial");
	
	var r = document.getElementById("dodaj_publikacje_rodzaj");
	var rodzaj = r.options[r.selectedIndex].value;
		
	if (rodzaj == 'K')
	{
		pokaz_pola_formularza_dodawania_publikacji_wg_rodzaju("dodaj_publikacje_ksiazka");
		document.getElementById("nowa_publikacja_data_wydania").required = true;
		document.getElementById("nowa_publikacja_wydawnictwo").required = true;
		document.getElementById("nowa_publikacja_miejsce_wydania").required = true;
	}
	if (rodzaj == 'A')
	{
		pokaz_pola_formularza_dodawania_publikacji_wg_rodzaju("dodaj_publikacje_artykul");
		document.getElementById("nowa_publikacja_data_publikacji").required = true;
		document.getElementById("nowa_publikacja_czasopismo").required = true;
		document.getElementById("nowa_publikacja_nr_czasopisma").required = true;
	}
	if (rodzaj == 'M')
	{
		pokaz_pola_formularza_dodawania_publikacji_wg_rodzaju("dodaj_publikacje_materialy");
		document.getElementById("nowa_publikacja_nazwa_konferencji").required = true;
		document.getElementById("nowa_publikacja_data_konferencji").required = true;
		document.getElementById("nowa_publikacja_lokalizacja_konferencji").required = true;
	}
	if (rodzaj == 'W')
	{
		pokaz_pola_formularza_dodawania_publikacji_wg_rodzaju("dodaj_publikacje_witryna");
		document.getElementById("nowa_publikacja_adres_url").required = true;
		document.getElementById("nowa_publikacja_data_odwiedzin").required = true;
	}
	if (rodzaj == 'R')
	{
		pokaz_pola_formularza_dodawania_publikacji_wg_rodzaju("dodaj_publikacje_rozdzial");
	}
}

function ukryj_pola_formularza_dodawania_publikacji_wg_rodzaju(rodzaj)
{
	var list = document.getElementsByClassName(rodzaj);
	for (var i = 0; i < list.length; i++) 
	{
		var l = list[i];
		l.style.display = "none";
	}
}

function pokaz_pola_formularza_dodawania_publikacji_wg_rodzaju(rodzaj)
{
	var list = document.getElementsByClassName(rodzaj);
	for (var i = 0; i < list.length; i++) 
	{
		var l = list[i];
		l.style.display = "table-row";
	}
}

function sprawdz_formularz_dodaj_publikacje()
{
	var uwaga = "";
	
	var tytul = document.getElementById("nowa_publikacja_tytul").value;
	if (tytul == "")
	{
		uwaga += "Podaj tytuł.\n";
	}
	var a = document.getElementById("dodaj_publikacje_autor");
	var autor = a.options[a.selectedIndex].value;
	if (autor == "wybierz")
	{
		uwaga += "Wybierz autora.\n";
	}
	var d = document.getElementById("dodaj_publikacje_dziedzina");
	var dziedzina = d.options[d.selectedIndex].value;
	if (dziedzina == "wybierz")
	{
		uwaga += "Wybierz dziedzinę.\n";
	}
	var j = document.getElementById("dodaj_publikacje_jezyk");
	var jezyk = j.options[j.selectedIndex].value;
	if (jezyk == "wybierz")
	{
		uwaga += "Wybierz język.\n";
	}
	var r = document.getElementById("dodaj_publikacje_rodzaj");
	var rodzaj = r.options[r.selectedIndex].value;
	if (rodzaj == "wybierz")
	{
		uwaga += "Wybierz rodzaj.\n";
	}
	
	if (uwaga == "")
	{
		return true;
	}
	else
	{
		alert(uwaga);
		return false;
	}
}

function modyfikuj_publikacje_w_kolekcji_przycisk(id)
{
	var paragraf = document.getElementById(id);
	if (paragraf != null)
	{
		if (paragraf.style.display == 'none')
			$('#'+id).slideDown();
		else 
			$('#'+id).slideUp();
	}
}

function pokaz_dodawanie_do_kolekcji()
{
	var div = document.getElementById("publikacja_dodaj_do_kolekcji");
	if (div.style.display == 'none')
		$('#publikacja_dodaj_do_kolekcji').slideDown();
	else 
		$('#publikacja_dodaj_do_kolekcji').slideUp();
}