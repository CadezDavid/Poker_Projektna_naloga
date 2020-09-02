import random
import itertools
import collections

#OZNAKE
#zapis karte: (stevilo, znak)
znaki = ['KARA', 'KRIZ', 'SRCE', 'PIK']
stevila = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

oznake_slike = {
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '10',
    11: 'J',
    12: 'Q',
    13: 'K',
    14: 'A',
    'KARA': 'D',
    'KRIZ': 'C',
    'SRCE': 'H',
    'PIK': 'S'
}

seznam_slik_igralcev = ['bonomo', 'ivey', 'kenney', 'negreanu', 'nekdo1', 'nekdo2', 'nekdo3', 'nekdo4', 'volpe', 'holz', 'brunson', 'hellmuth', 'chidwick', 'esfandiari']

def alternativni_zapis(karta):
    if karta == 'Neodprta':
        return karta
    return str(oznake_slike[karta[0]]) + str(oznake_slike[karta[1]])

def nov_kup():
    kup = list()
    for znak in znaki:
        for stevilo in stevila:
            kup.append((stevilo, znak))
    random.shuffle(kup)
    return kup


#PRIMERJANJE DVEH SEDMERIC

def na_dva_dela(karte):
    'Razdeli peterico na seznam števil in seznam znakov.'
    znaki_trenutni = list()
    stevila_trenutna = list()
    for karta in karte:
        stevila_trenutna.append(karta[0])
        znaki_trenutni.append(karta[1])
    return stevila_trenutna, znaki_trenutni

def kolikokrat_se_pojavi_katera_stevilka(karte):
    'Vrne seznam, kjer so v ključih števila, v vrednostih pa število ponovitev.'
    return dict(collections.Counter(na_dva_dela(karte)[0]))

def tvorijo_lestvico(karte):
    'Preveri, če peterica tvori lestvico.'
    karte_stevila = na_dva_dela(karte)[0]
    if 14 not in karte:
        return sorted(karte_stevila) == list(range(min(karte_stevila), max(karte_stevila) + 1))
    else:
        return all([stevilo in karte_stevila for stevilo in range(2, 6)]) or \
            all([stevilo in karte_stevila for stevilo in range(10, 15)])

def tvorijo_kraljevo_lestvico(karte):
    'Preveri, če tvorjo barvno lestvico, ki se začne z 10 in konča za Asom.'
    return tvorijo_barvo(karte) and all([stevilo in na_dva_dela(karte)[0] for stevilo in range(10, 15)])

def tvorijo_barvo(karte):
    return len(set(na_dva_dela(karte)[1])) == 1

def poker(karte):
    for stevilka in na_dva_dela(karte)[0]:
        if kolikokrat_se_pojavi_katera_stevilka(karte)[stevilka] == 4:
            return [True, stevilka]
    return [False]

def full_house(karte):
    if set(kolikokrat_se_pojavi_katera_stevilka(karte).values()) == {2, 3}:
        rezultat = [True, 0, 0]
        for stevilka in kolikokrat_se_pojavi_katera_stevilka(karte).keys():
            if kolikokrat_se_pojavi_katera_stevilka(karte)[stevilka] == 3:
                rezultat[1] = stevilka
            else:
                rezultat[2] = stevilka
        return rezultat
    return [False]

def tris(karte):
    if set(kolikokrat_se_pojavi_katera_stevilka(karte).values()) == {3, 1, 1}:
        for karta in kolikokrat_se_pojavi_katera_stevilka(karte).keys():
            if kolikokrat_se_pojavi_katera_stevilka(karte)[karta] == 3:
                return [True, karta]
    return [False]

def dva_para(karte):
    if set(kolikokrat_se_pojavi_katera_stevilka(karte).values()) == {2, 2, 1}:
        rezultat = [True, 0, 0]
        for karta in kolikokrat_se_pojavi_katera_stevilka(karte).keys():
            if kolikokrat_se_pojavi_katera_stevilka(karte)[karta] == 2:
                if rezultat[1] < karta:
                    rezultat[2] = rezultat[1]
                    rezultat[1] = karta
                else:
                    rezultat[2] = karta
        return rezultat
    return [False]

def par(karte):
    if set(kolikokrat_se_pojavi_katera_stevilka(karte).values()) == {2, 1, 1, 1}:
        for karta in kolikokrat_se_pojavi_katera_stevilka(karte).keys():
            if kolikokrat_se_pojavi_katera_stevilka(karte)[karta] == 2:
                return [True, karta[0]]
    return [False]

def vrednost(karte):
    'Peterici priredimo seznam dolžine 3.'
    if tvorijo_kraljevo_lestvico(karte):
        return [10, 0, 0]
    elif tvorijo_lestvico(karte) and tvorijo_barvo(karte):
        return [9, max(karte, key=lambda x: x[0]), 0]
    elif poker(karte)[0]:
        return [8, poker(karte)[1], 0]
    elif full_house(karte)[0]:
        return [7, full_house(karte)[1], full_house(karte)[2]]
    elif tvorijo_barvo(karte):
        return [6, 0, 0]
    elif tvorijo_lestvico(karte):
        return [5, max(karte, key=lambda x: x[0]), 0]
    elif tris(karte)[0]:
        return [4, tris(karte), 0]
    elif dva_para(karte)[0]:
        return [3, dva_para(karte)[1], dva_para(karte)[2]]
    elif par(karte)[0]:
        return [2, par(karte)[1], 0]
    else:
        return [1, max(karte, key=lambda x: x[0]), 0]

def najvisjih_pet(karte):
    'Vrne najvišjih pet iz sedmerice.'
    return sorted(karte, key=lambda x: x[0])[0:5]

def visja_karta(peterica1, peterica2):
    'Izbere peterico, ki zmaga z višjo karto.'
    for indeks in range(5):
        if peterica1[indeks][0] < peterica2[indeks][0]:
            return 2
        elif peterica1[indeks][0] > peterica2[indeks][0]:
            return 1
    return 0

def vrednost_sedmerice(karte):
    'Vrne najvišjo peterico.'
    najvisja = [0, 0, 0]
    for peterica in itertools.combinations(karte, 5):
        peterica = list(peterica)
        if najvisja < vrednost(peterica):
            najvisja = vrednost(peterica)
    return najvisja

def primerjaj_sedmerici(karte1, karte2):
    if vrednost_sedmerice(karte1) > vrednost_sedmerice(karte2):
        return 1
    elif vrednost_sedmerice(karte1) < vrednost_sedmerice(karte2):
        return 2
    elif najvisjih_pet(karte1) > najvisjih_pet(karte2):
        return 1
    elif najvisjih_pet(karte1) < najvisjih_pet(karte2):
        return 2
    else:
        return 0

def equal_sez(seznam):
    return seznam[1:] == seznam[:-1]

def seznam_začenši_z_n_tim(seznam, n):
    return seznam[n:] + seznam[:n]