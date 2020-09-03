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

    if soba.preveri_izid():
        bottle.redirect('/konec_igre/' + str(id_sobe) + '/')

    soba.trenutna_igra = Igra(soba.igralci_za_mizo, soba.denar)
    print(soba.trenutna_igra.kup)
    print(soba.trenutna_igra.igralci)
    soba.trenutna_igra.razdeli_karte()
    soba.izvedi_nujne_stave()
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

    assert soba.trenutna_igra.denar[ime] >= stava

    soba.trenutna_igra.igralec_visa_za(ime, stava)

    soba.trenutna_igra.premakni_potezo()

    if soba.preveri_izid():
        bottle.redirect('/konec_igre/' + str(id_sobe) + '/')

    if soba.trenutna_igra.igralci[soba.trenutna_igra.na_potezi] == soba.ime_igralca:
        bottle.redirect('/igra/' + str(id_sobe) + '/')
    else:
        bottle.redirect('/igra/racunalnikovi_manevri/' + str(id_sobe) + '/')
    

@bottle.post('/igra/fold/<id_sobe>/')
def fold_igra(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]

    ime = soba.ime_igralca

    soba.trenutna_igra.igralec_folda(ime)

    soba.trenutna_igra.premakni_potezo()

    soba.trenutna_igra.preveri_zmaga()

    if soba.preveri_izid():
        bottle.redirect('/konec_igre/' + str(id_sobe) + '/')

    if soba.trenutna_igra.igralci[soba.trenutna_igra.na_potezi] == soba.ime_igralca:
        bottle.redirect('/igra/' + str(id_sobe) + '/')
    else:
        bottle.redirect('/igra/racunalnikovi_manevri/' + str(id_sobe) + '/')

@bottle.post('/igra/equal/<id_sobe>/')
def izenaci_igra(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]

    ime = soba.ime_igralca

    soba.trenutna_igra.igralec_izenaci(ime)

    soba.trenutna_igra.premakni_potezo()

    soba.trenutna_igra.preveri_zmaga()

    if soba.trenutna_igra.igralci[soba.trenutna_igra.na_potezi] == soba.ime_igralca:
        bottle.redirect('/igra/' + str(id_sobe) + '/')
    else:
        bottle.redirect('/igra/racunalnikovi_manevri/' + str(id_sobe) + '/')

@bottle.post('/igra/check/<id_sobe>/')
def check_igra(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]

    soba.trenutna_igra.premakni_potezo()

    soba.trenutna_igra.preveri_zmaga()

    if soba.preveri_izid():
        bottle.redirect('/konec_igre/' + str(id_sobe) + '/')

    if soba.trenutna_igra.igralci[soba.trenutna_igra.na_potezi] == soba.ime_igralca:
        bottle.redirect('/igra/' + str(id_sobe) + '/')
    else:
        bottle.redirect('/igra/racunalnikovi_manevri/' + str(id_sobe) + '/')

@bottle.get('/igra/racunalnikovi_manevri/<id_sobe>/')
def racunalnik_igra(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]

    oseba_na_potezi = soba.trenutna_igra.ime_osebe_na_potezi()

    izvedi_smiselno_potezo(soba.trenutna_igra, oseba_na_potezi)

    soba.trenutna_igra.premakni_potezo()

    soba.trenutna_igra.preveri_zmaga()
    
    if soba.preveri_izid():
        bottle.redirect('/konec_igre/' + str(id_sobe) + '/')

    bottle.redirect('/igra/' + str(id_sobe) + '/')

@bottle.get('/konec_igre/<id_sobe>/')
def konec_igre(id_sobe):
    id_sobe = int(id_sobe)
    soba = slovar_sob[id_sobe]
    izid = soba.preveri_izid()
    return bottle.template('konec_igre.tpl', izid=izid)

@bottle.get('/Slike/<slika>')
def slike(slika):
    return bottle.static_file(slika, root='Slike')

bottle.run(debug=True, reloader=True)