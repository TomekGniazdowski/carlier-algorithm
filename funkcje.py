import copy
import numpy as np

def konwersja_str_int(s):
    for i in range(len(s)):
        s[i] = int(s[i])
    return s


def odczyt_pliku(nazwa_pliku):
    f = open(nazwa_pliku, 'r')
    r = []
    p = []
    q = []
    n = 0
    wszystkie_linie = f.readlines()
    for licznik, linia in enumerate(wszystkie_linie):
        if licznik == 0:
            n = linia.rstrip('\n')
        else:
            s = linia.rstrip('\n').split(' ')
            r.append(s[0])
            p.append(s[1])
            q.append(s[2])
    f.close()
    lst = []
    for i in range(0, len(r)):
        lst.append((int(r[i]), int(p[i]), int(q[i])))
    return int(n), konwersja_str_int(r), konwersja_str_int(p), konwersja_str_int(q), sorted(lst, key=lambda  x:x[0])


def wyswietl_plik(n, r, p, q):
    for i in range(0, len(r) + 1):
        if i == 0:
            print(n)
        elif i > 0:
            print(r[i - 1], p[i - 1], q[i - 1])


def spr_wynik(nazwa_pliku, rzeczywisty_wynik):
    f = open(nazwa_pliku, 'r')
    poprawny_wynik = konwersja_str_int(f.readlines())[0]
    f.close()
    if poprawny_wynik == rzeczywisty_wynik:
        return True
    else:
        return False


def schrage(n, r, p, q):
    C = []
    r_copy = []
    p_copy = []
    q_copy = []
    b = 0
    t = 0
    k = 0
    Cmax = 0
    G = []
    permutacja = []
    _permutacja = []
    N = [(i, r[i]) for i in range(0, n)]
    N = sorted(N, key=lambda x: x[1], reverse=False)

    while len(G) != 0 or len(N) != 0:
        while len(N) != 0 and N[0][1] <= t:
            e = N[0][0]
            G.append((e, q[e]))
            N.pop(0)
        if len(G) == 0:
            t = N[0][1]
        else:
            G = sorted(G, key=lambda x: x[1], reverse=True)
            e = G[0][0]
            G.pop(0)
            permutacja.append(e)
            t = t + p[e]
            C.append(t)
            Cmax = max(Cmax, t + q[e])
            k = k + 1
    for e in permutacja:
        r_copy.append(r[e])
        p_copy.append(p[e])
        q_copy.append(q[e])
    _permutacja = [r_copy, p_copy, q_copy]
    return Cmax, C, _permutacja


def schrage_z_podzialem(n, r, p, q):
    t = 0
    Cmax = 0
    G = []
    N = [(i, r[i]) for i in range(0, n)]
    N = sorted(N, key=lambda x: x[1], reverse=False)
    l = 0

    while len(G) != 0 or len(N) != 0:
        while len(N) != 0 and N[0][1] <= t:
            e = N[0][0]
            G.append((e, q[e]))
            N.pop(0)
            if q[e] > q[l]:
                p[l] = t - r[e]
                t = r[e]
                if p[l] > 0:
                    G.append((l, q[l]))
        if len(G) == 0:
            t = N[0][1]
        else:
            max_q = max(G, key=lambda x: x[1])
            e = max_q[0]
            G.pop(G.index(max_q))
            l = e
            t = t + p[e]
            Cmax = max(Cmax, t + q[e])
    return Cmax

class Carlier:
    def __init__(self, n):
        self.UB = 10000000
        self.opt_r = [x for x in range(n)]
        self.opt_p = [x for x in range(n)]
        self.opt_q = [x for x in range(n)]

    def carlier(self, n, r, p, q):
        U, C, _lst = schrage(n, copy.deepcopy(r), copy.deepcopy(p), copy.deepcopy(q))
        r = copy.deepcopy(_lst[0])
        p = copy.deepcopy(_lst[1])
        q = copy.deepcopy(_lst[2])
        if U < self.UB:
            self.UB = U
            self.opt_r = copy.deepcopy(_lst[0])
            self.opt_q = copy.deepcopy(_lst[1])
            self.opt_p = copy.deepcopy(_lst[2])
        b = zwroc_b(U, C, n, q)
        a = zwroc_a(U, b, n, r, p, q)
        c = zwroc_c(a, b, q)
        if c is None:
            return self.UB
        _r = min(r[c + 1:b + 1])
        _p = sum(p[c + 1:b + 1])
        _q = min(q[c + 1:b + 1])
        r_c = r[c]
        r[c] = max(r[c], _r + _p)
        LB = schrage_z_podzialem(n, copy.deepcopy(r), copy.deepcopy(p), copy.deepcopy(q))
        if LB < self.UB:
            self.carlier(n, copy.deepcopy(r), copy.deepcopy(p), copy.deepcopy(q))
        r[c] = r_c
        q_c = q[c]
        q[c] = max(q[c], _q + _p)
        LB = schrage_z_podzialem(n, copy.deepcopy(r), copy.deepcopy(p), copy.deepcopy(q))
        if LB < self.UB:
            self.carlier(n, copy.deepcopy(r), copy.deepcopy(p), copy.deepcopy(q))
        q[c] = q_c
        return self.UB

def zwroc_b(Cmax, C, n, q):
    b = -1
    for j in range(0, n):
        if Cmax == C[j] + q[j]:
            b = j
    return b

def zwroc_a(Cmax, b, n, r, p, q):
    a = 0
    for j in range(0, n):
        if Cmax == r[j] + sum(p[j:b+1]) + q[b]:
            a = j
            return a
    return a

def zwroc_c(a, b, q):
    c = -1
    for j in range(a, b + 1):
        if q[j] < q[b]:
            c = j
    if c != -1:
        return c
    if c == -1:
        return None
