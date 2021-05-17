import funkcje as fu
import time

for i in range(1, 11):
    il_zadan, termin_dostepnosci, czas_wykonania, czas_dostarczenia, lst = fu.odczyt_pliku(f'Input/SCHRAGE{i}.DAT')
    #fu.wyswietl_plik(il_zadan, termin_dostepnosci, czas_wykonania, czas_dostarczenia)
    cr = fu.Carlier(il_zadan)
    start = time.time()
    wynik = cr.carlier(il_zadan, termin_dostepnosci, czas_wykonania, czas_dostarczenia)
    stop = time.time()
    if fu.spr_wynik(f'Output/SCHRAGE{i}.DAT', wynik) is True:
        print(f'Calier{i} ->', wynik, '\u2713', stop - start, 's')
    else:
        print(f'Calier{i} ->', wynik, '\u2717')
