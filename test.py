# Carlier

from operator import itemgetter
import copy
import timeit
import time


class PriorityQueue:

    def __init__(self, key, rev, l):
        self._key = key
        self._rev = rev
        if len(l) == 0:
            self._list = []
        else:
            self._list = l.sort(key=key, reverse=rev)

    def delete(self):
        self._list.pop(len(self._list) - 1)

    def add(self, val):
        self._list.append(val)
        self._list.sort(key=self._key, reverse=self._rev)
        # print(f"key = {self._key}, list = {self._list}")

    def display(self):
        print(self._list)

    def return_list(self):
        return self._list

    def is_empty(self):
        if len(self._list) == 0:
            return True
        else:
            return False

    def get_element(self):
        return self._list[len(self._list) - 1]

    def get_r(self, nb):
        # print("r getted")
        return self._list[len(self._list) - 1][0]


def read(nb):
    lst = []
    with open('data\\SCHRAGE' + str(nb) + '.DAT') as f:
        f.readline()  # pominięcie n
        for i in f:
            x, y, z = i.split()
            lst.append([int(x), int(y), int(z)])
    return sorted(lst, key=lambda i: i[0])  # sortowanie po r


def get_anwser(nb):
    with open('data\\CARLIER' + str(nb) + '.OUT') as f:
        x = f.readline()  # pominięcie n
    return x


def schrage(data):
    t = 0
    k = 0
    b = 0  # indeks zadania z cmaxem w permutacji
    N = PriorityQueue(itemgetter(0), True, [])
    G = PriorityQueue(itemgetter(2), False, [])

    C_max = 0
    pi = []

    for i in range(0, len(data)):
        N.add([int(data[i][0]), int(data[i][1]), int(data[i][2])])

    while G.is_empty() is False or N.is_empty() is False:  # 2
        while N.is_empty() is False and int(N.get_r(0)) <= t:  # 3
            e = N.get_element()
            G.add(e)
            N.delete()
        if G.is_empty() is True:  # 5
            t = int(N.get_r(0))  # 6
        else:
            e = G.get_element()
            G.delete()
            pi.append(e)
            t += int(e[1])
            if C_max <= int(t + int(e[2])):
                C_max = int(t + int(e[2]))
                b = k
            k += 1

    return pi, C_max, b


def schrage_div(data):
    n = len(data)
    t = 0  # total time
    N = PriorityQueue(itemgetter(0), True, [])  # list of unordered tasks
    G = PriorityQueue(itemgetter(2), False, [])  # list of ready to implementation tasks

    C_max = 0
    pi = []

    for i in range(0, n):
        N.add([int(data[i][0]), int(data[i][1]), int(data[i][2])])

    onMachine = [0, 0, 999999]  # current task initialization

    while G.is_empty() is False or N.is_empty() is False:  # check if at least one OR lists isn't empty
        while N.is_empty() is False and int(
                N.get_r(0)) <= t:  # check if N isn't empty AND availability time is less than total time
            e = N.get_element()  # ready task
            G.add(e)
            N.delete()
            if e[2] > onMachine[2]:  # check if time to complete ready task is higher than time on machine
                onMachine[1] = t - e[0]
                t = e[0]
                if onMachine[1] > 0:
                    G.add(onMachine)

        if G.is_empty() is True:  # 5
            t = int(N.get_r(0))  # 6
        else:
            e = G.get_element()
            G.delete()
            onMachine = e
            pi.append(e)
            t += int(e[1])
            C_max = max(C_max, int(t + int(e[2])))

    return C_max


def findA(lst, b, Cmax):
    sum = a = 0
    for i in range(0, b + 1):
        sum += lst[i][1]

    while a < b and not Cmax == (lst[a][0] + lst[b][2] + sum):
        sum -= lst[a][1]
        a += 1
    return a


def findC(lst, a, b):
    for i in range(b - 1, a - 1, -1):
        if lst[i][2] < lst[b][2]:
            return i
    return None


def findRPQprim(lst, b, c):
    rprim = lst[c + 1][0]
    pprim = 0
    qprim = lst[c + 1][2]

    for i in range(c + 1, b + 1):
        if lst[i][0] < rprim:
            rprim = lst[i][0]
        if lst[i][2] < qprim:
            qprim = lst[i][2]
        pprim += lst[i][1]

    return rprim, pprim, qprim


def carlier(lst):
    lst, Cmax, b = schrage(copy.deepcopy(
        lst))  # lst - permutacja zadań, C-max - górne oszacowanie, b - pozycja ostatniego w ścieżce krytycznej
    a = findA(lst, b, Cmax)  # pozycja pierwszego zadania w ścieżce krytycznej
    c = findC(lst, a, b)  # zadanie o jak najwyższej pozycji ale z mniejszym q_pi_j < q_pi_b
    if not c:  # jeśli nie znaleziono takiego to c_max jest roziwązaniem optymalnym
        return Cmax

    rprim, pprim, qprim = findRPQprim(lst, b, c)  # min r, max q, suma czasów wykonania zadań - w bloku (c+1, b)
    r_saved = lst[c][0]  # zapisz r
    lst[c][0] = max(lst[c][0],
                    rprim + pprim)  # modyfikacja terminu dostępności zadania c, wymusi to jego późniejszą realizację, za wszystkimi zadaniami w bloku(c+1, b)
    LB = schrage_div(copy.deepcopy(
        lst))  # sprawdzamy dolne ograniczenie schrage z podziałem  - dla wszystkich permutacji spełniających to wymaganie

    if LB < Cmax:  # sprawdź czy rozwiązanie jest obiecujące
        Cmax = min(Cmax, carlier(lst))  # wywołaj carliera jeszcze raz dla nowego problemu

    lst[c][0] = r_saved  # odtwórz r

    q_saved = lst[c][2]
    lst[c][2] = max(lst[c][2],
                    pprim + qprim)  # wymuszenie aby zadanie c było wykonywane przed wszystkimi zadaniami w bloku (c+1, b)
    LB = schrage_div(copy.deepcopy(lst))  # sprawdź czy taki problem jest obiecujący

    if LB < Cmax:
        Cmax = min(Cmax, carlier(lst))

    lst[c][2] = q_saved  # przywróc q

    return Cmax


def test(start, end):
    for i in range(start, end + 1):
        tasks = read(i)
        start_time = time.time()
        result = carlier(tasks)
        execution_time = time.time() - start_time
        print('Carlier: ' + str(result) + ' | ' + 'Odp: ' + str(get_anwser(i)) + ' | Czas: ' + str(execution_time))


test(1, 10)