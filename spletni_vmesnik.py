import bottle
from poker import *
from bot import *
import random
import json

# datoteka_s_stanjem = 'stanje.json'

# hisa = Hisa(datoteka_s_stanjem)

slovar_sob = {0: None}

imena = list()
for ime in open('imena.txt', 'r').readlines():
    imena.append(ime.rstrip())

@bottle.get('/')
def home():
    return bottle.template('home.tpl')

@bottle.post('/home/')
def nov_poker():
    #Pridobi zahtevane podatke
    stevilo_racunalnikov = int(bottle.request.forms.getunicode('stevilo_racunalnikov'))
    ime_sobe = str(bottle.request.forms.getunicode('ime_sobe'))
    ime_igralca = str(bottle.request.forms.getunicode('ime_igralca'))
    zacetni_denar = int(bottle.request.forms.getunicode('zacetni_denar'))
    #Izbere id trenutne sobe
    id_sobe = max(slovar_sob.keys()) + 1
    #Definira nov Poker
    ime_sobe = Poker(ime_sobe, ime_igralca, stevilo_racunalnikov,zacetni_denar)
    #Shrani ga pod izbrani id_sobe, zaenkrat še nima igre
    slovar_sob[id_sobe] = [ime_sobe, None]
    #Preusmeri na igro
    print(slovar_sob)
    bottle.redirect('/zacetek_igre/' + str(id_sobe) + '/')

@bottle.get('/zacetek_igre/<id_sobe>/')
def nova_igra(id_sobe):
    print(slovar_sob)
    #Pridobi podatke o trenutnem pokru
    id_sobe = int(id_sobe)
    podatki_sobe = slovar_sob[id_sobe]
    #Sestavi seznam igralcev začenši s tistim, ki ima big blind žeton
    trenutni_igralci = seznam_začenši_z_n_tim(podatki_sobe[0].igralci, podatki_sobe[0].pozicija_big_blind)
    #Ustvari slovar denarja
    #Ustvari igro in razdeli karte
    trenutna_igra = Igra(trenutni_igralci, podatki_sobe[0].denar)
    slovar_sob[id_sobe][1] = trenutna_igra
    trenutna_igra.razdeli_karte()
    return bottle.template('igra.tpl', ime_sobe=podatki_sobe[0], igra=podatki_sobe[1], id_sobe=id_sobe)

@bottle.get('/igra/<id_sobe>/')
def igra(id_sobe):
    #Najprej je treba za id zacet uporabljat integer
    id_sobe = int(id_sobe)
    #Z id-jem pridobi podatke sobe
    podatki_sobe = slovar_sob[id_sobe]
    
    return bottle.template('igra.tpl', ime_sobe=podatki_sobe[0], igra=podatki_sobe[1], id_sobe=id_sobe)

@bottle.post('/igra/stava/<id_sobe>/')
def stava_igra(id_sobe):
    #Pridobi podatke o trenutni situaciji
    id_sobe = int(id_sobe)
    podatki_sobe = slovar_sob[id_sobe]

    #Pridobi podatke o stavi
    stava = int(bottle.request.forms.getunicode('Stava'))

    #To pot uporabi le igralec
    ime = podatki_sobe[0].ime_igralca

    assert podatki_sobe[1].denar[ime] >= stava

    #Igralcu povisamo stavo
    podatki_sobe[1].igralec_visa_na(ime, stava)

    #Premaknemo potezo, s tem se lahko odprejo nove karte
    podatki_sobe[1].premakni_potezo()

    #Preverimo ali je naslednji na vrsti računalnik ali pa oseba
    if podatki_sobe[1].igralci[podatki_sobe[1].na_potezi] == podatki_sobe[0].ime_igralca:
        bottle.redirect('/igra/' + str(id_sobe) + '/')
    else:
        bottle.redirect('/igra/racunalnikovi_manevri/' + str(id_sobe) + '/')
    

@bottle.post('/igra/fold/<id_sobe>/')
def fold_igra(id_sobe):
    #Pridobi podatke o trenutni situaciji
    id_sobe = int(id_sobe)
    podatki_sobe = slovar_sob[id_sobe]

    #To pot uporabi le igralec
    ime = podatki_sobe[0].ime_igralca

    #Igralec na potezi je foldal, treba ga je odstraniti iz trenutne igre
    podatki_sobe[1].igralec_folda(ime)

    #Premaknemo potezo, s tem se lahko odprejo nove karte
    podatki_sobe[1].premakni_potezo()

    #Preverimo ali je naslednji na vrsti računalnik ali pa oseba
    if podatki_sobe[1].igralci[podatki_sobe[1].na_potezi] == podatki_sobe[0].ime_igralca:
        bottle.redirect('/igra/' + str(id_sobe) + '/')
    else:
        bottle.redirect('/igra/racunalnikovi_manevri/' + str(id_sobe) + '/')

@bottle.post('/igra/check/<id_sobe>/')
def check_igra(id_sobe):
    #Pridobi podatke o trenutni situaciji
    id_sobe = int(id_sobe)
    podatki_sobe = slovar_sob[id_sobe]

    #Premaknemo potezo, s tem se lahko odprejo nove karte
    podatki_sobe[1].premakni_potezo()

    #Preverimo ali je naslednji na vrsti računalnik ali pa oseba
    if podatki_sobe[1].igralci[podatki_sobe[1].na_potezi] == podatki_sobe[0].ime_igralca:
        bottle.redirect('/igra/' + str(id_sobe) + '/')
    else:
        bottle.redirect('/igra/racunalnikovi_manevri/' + str(id_sobe) + '/')

@bottle.get('/igra/racunalnikovi_manevri/<id_sobe>/')
def racunalnik_igra(id_sobe):
    #Pridobi podatke o trenutni situaciji
    id_sobe = int(id_sobe)
    podatki_sobe = slovar_sob[id_sobe]

    #Razberi osebo na potezi
    oseba_na_potezi = podatki_sobe[1].igralci[podatki_sobe[1].na_potezi]

    #Oseba naključno viša za 10 ali pa checka
    if random.choice([False, False, False, False, False, True]):
        podatki_sobe[1].igralec_visa_na(oseba_na_potezi, random.randint(1, 100))
    else:
        podatki_sobe[1].igralec_izenaci(oseba_na_potezi)

    #Premakni potezo
    podatki_sobe[1].premakni_potezo()

    print(podatki_sobe[1].igralci[podatki_sobe[1].na_potezi])
    
    #Preverimo ali je naslednji na vrsti računalnik ali pa oseba
    # if podatki_sobe[1].igralci[podatki_sobe[1].na_potezi] == podatki_sobe[0].ime_igralca:
    bottle.redirect('/igra/' + str(id_sobe) + '/')


bottle.run(debug=True, reloader=True)