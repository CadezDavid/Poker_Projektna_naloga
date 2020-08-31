from funkcije import *
import bottle
import json
import random


class Poker:

    def __init__(self, ime, ime_igralca, stevilo_racunalnikov=3, zacetni_denar=10**3):
        with open('imena.txt', 'r') as dat:
            imena = [ime.rstrip() for ime in dat.readlines()]
        self.ime = ime
        self.ime_igralca = ime_igralca
        self.stevilo_igralcev_za_mizo = stevilo_racunalnikov + 1
        self.stevilo_racunalnikov = stevilo_racunalnikov
        self.igralci = [ime_igralca] + random.sample(imena, stevilo_racunalnikov)
        self.zacetni_denar = zacetni_denar
        self.big_blind = 10
        self.small_blind = 5
        self.pozicija_big_blind = 2 % self.stevilo_igralcev_za_mizo
        self.pozicija_small_blind = 1 % self.stevilo_igralcev_za_mizo
        self.minimalno_na_mizi = 10
        self.denar = {igralec: zacetni_denar for igralec in self.igralci}
    
    def odstrani_igralce(self):
        'Odstrani igralce, ki nimajo več denarja, in na novo definira število njih.'
        self.igralci = [igralec for igralec in self.igralci if self.denar[igralec] > 0]
        self.stevilo_igralcev_za_mizo = len(self.igralci)

    def stave_zmagovalcu(self, zmagovalec, igra):
        self.denar[zmagovalec] += igra.sestej_stave()
    
    def konec_igre(self, zmagovalec):
        return f'Konec igre. Zmagal je {zmagovalec.ime}'

class Igra:

    def __init__(self, igralci, denar, big_blind=10, small_blind=5):
        #Igra bo definirana tako, da se bo seznam igralcev začel s tistim, ki ima žeton big blind
        self.igralci = igralci
        #Odsek: 0 - preflop, 1 - flop, 2 - turn, 3 - river
        self.odsek = 0
        self.na_potezi = 0
        self.big_blind = big_blind
        #Denar je slovar, kjer so ključi igralci in vrednosti njihov denar
        self.denar = denar
        self.small_blind = small_blind
        self.karte_na_mizi = [None, None, None, None, None]
        self.karte_igralcev = dict()
        self.igralci_v_igri = {igralec: True for igralec in self.igralci}
        self.kup = nov_kup()
        self.stava = {igralec: 0 for igralec in self.igralci}
        self.min_na_mizi = max([self.stava[igralec] for igralec in self.igralci])

    def sestej_in_odstrani_stave(self):
        'Sešteje stave in odstrani vse stave.'
        vsota = 0
        for igralec in self.igralci:
            vsota += self.stava[igralec]
            self.stava[igralec] = 0
        return vsota

    def igralec_folda(self, igralec):
        self.igralci_v_igri[igralec] = False
    
    def stevilo_igralcev_v_igri(self):
        return sum(list(self.igralci_v_igri.values()))
    
    def igralec_visa_na(self, igralec, vsota):
        #Igralec poveca svojo stavo na podano vsoto
        if vsota <= self.min_na_mizi:
            self.igralec_izenaci(igralec)
        else:
            self.stava[igralec] = vsota
            self.denar[igralec] -= vsota
        self.min_na_mizi = max([self.stava[igralec] for igralec in self.igralci])
    
    def igralec_izenaci(self, igralec):
        self.denar[igralec] -= self.min_na_mizi - self.stava[igralec]
        self.stava[igralec] = self.min_na_mizi
    
    def premakni_potezo(self):
        'Premakne potezo na naslednjega igralca v igri. Pri tem mogoče začne nov odsek igre in zato odpre dodatne karte.'
        if self.na_potezi + 1 == len(self.igralci):
            if self.vse_stave_enake():
                self.odsek += 1
                self.odpri_dodatne_karte()
                self.na_potezi = 0
            else:
                self.na_potezi = 0
        else:
            self.na_potezi += 1
            self.na_potezi = self.na_potezi % len(self.igralci)
            while not self.igralci_v_igri[self.igralci[self.na_potezi]]:
                self.na_potezi += 1
                self.na_potezi = self.na_potezi % len(self.igralci)

    def razdeli_karte(self):
        for igralec in self.igralci:
            self.karte_igralcev[igralec] = [self.kup.pop() for _ in range(2)]

    def flop(self):
        self.karte_na_mizi[0:3] = [self.kup.pop() for _ in range(3)]
    
    def turn(self):
        self.karte_na_mizi[3] = self.kup.pop()
    
    def river(self):
        self.karte_na_mizi[4] = self.kup.pop()

    def odpri_dodatne_karte(self):
        if self.odsek == 1:
            self.flop()
        elif self.odsek == 2:
            self.turn()
        elif self.odsek == 3:
            self.river()

    def vse_stave_enake(self):
        return all([self.stava[igralec] == self.stava[list(self.stava.keys())[0]] for igralec in self.igralci if self.igralci_v_igri[igralec]])