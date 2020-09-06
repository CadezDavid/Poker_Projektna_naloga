import bottle
from poker import *
from bot import *
import random
import json

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
    ime_igralca = str(bottle.request.forms.getunicode('ime_igralca'))
    zacetni_denar = int(bottle.request.forms.getunicode('zacetni_denar'))
    #Izbere id trenutne sobe
    id_sobe = random.randint(10 ** 10, 10 ** 11)
    while id_sobe in slovar_sob:
        id_sobe = random.randint(10 ** 10, 10 ** 11)
    #Definira nov Poker in ga shrani pod izbrani id_sobe, zaenkrat še nima igre
    slovar_sob[id_sobe] = Poker(ime_igralca, stevilo_racunalnikov, zacetni_denar)
    #Preusmeri na igro
    bottle.redirect('/zacetek_igre/' + str(id_sobe) + '/')

@bottle.get('/zacetek_igre/<id_sobe>/')
def nova_igra(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]

    if soba.trenutna_igra:
        soba.nova_igra(soba.trenutna_igra.denar)
    else:
        soba.prva_igra()

    if soba.preveri_izid()[0]:
        bottle.redirect('/konec_sobe/' + str(id_sobe) + '/')

    soba.trenutna_igra.razdeli_karte()
    soba.trenutna_igra.izvedi_nujne_stave()
    
    return bottle.template('igra.tpl', soba=soba, id_sobe=id_sobe)

@bottle.get('/igra/<id_sobe>/')
def igra(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]
    
    return bottle.template('igra.tpl', soba=soba, id_sobe=id_sobe)

@bottle.post('/igra/stava/<id_sobe>/')
def stava_igra(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]

    stava = int(bottle.request.forms.getunicode('Stava'))
    ime = soba.ime_igralca

    soba.trenutna_igra.igralec_visa_za(ime, stava)

    soba.trenutna_igra.premakni_potezo()

    if soba.preveri_izid()[0]:
        bottle.redirect('/konec_sobe/' + str(id_sobe) + '/')

    bottle.redirect('/igra/' + str(id_sobe) + '/')
    

@bottle.post('/igra/odstop/<id_sobe>/')
def odstop_igra(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]

    ime = soba.ime_igralca

    soba.trenutna_igra.igralec_folda(ime)

    soba.trenutna_igra.premakni_potezo()

    if soba.preveri_izid()[0]:
        bottle.redirect('/konec_sobe/' + str(id_sobe) + '/')

    bottle.redirect('/igra/' + str(id_sobe) + '/')

@bottle.post('/igra/izenaci/<id_sobe>/')
def izenaci_igra(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]

    ime = soba.ime_igralca

    soba.trenutna_igra.igralec_izenaci(ime)

    soba.trenutna_igra.premakni_potezo()

    bottle.redirect('/igra/' + str(id_sobe) + '/')

@bottle.post('/igra/naprej/<id_sobe>/')
def naprej_igra(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]

    soba.trenutna_igra.premakni_potezo()

    if soba.preveri_izid()[0]:
        bottle.redirect('/konec_sobe/' + str(id_sobe) + '/')

    bottle.redirect('/igra/' + str(id_sobe) + '/')


@bottle.get('/igra/racunalnikovi_manevri/<id_sobe>/')
def racunalnik_igra(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]

    oseba_na_potezi = soba.trenutna_igra.ime_osebe_na_potezi()

    drznost = soba.drznost[oseba_na_potezi]

    izvedi_smiselno_potezo(soba.trenutna_igra, oseba_na_potezi, drznost)

    soba.trenutna_igra.premakni_potezo()

    print(soba.trenutna_igra.na_potezi)
    print(soba.trenutna_igra.zaporedni_krog)
    print(soba.trenutna_igra.odsek)
    print(soba.trenutna_igra.zadnji_igralec_v_krogu())

    if soba.preveri_izid()[0]:
        bottle.redirect('/konec_sobe/' + str(id_sobe) + '/')

    bottle.redirect('/igra/' + str(id_sobe) + '/')

@bottle.get('/konec_sobe/<id_sobe>/')
def konec_igre(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]
    izid = soba.preveri_izid()[1]
    return bottle.template('konec_sobe.tpl', izid=izid)

@bottle.get('/Slike/<slika>')
def slike(slika):
    return bottle.static_file(slika, root='Slike')

bottle.run(debug=True, reloader=True)