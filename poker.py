from funkcije import *
import bottle
import json
import random


class Poker:

    def __init__(self, ime_igralca, stevilo_racunalnikov=3, zacetni_denar=2*10**3):
        with open('imena.txt', 'r') as dat:
            imena = [ime.rstrip() for ime in dat.readlines()]
        self.igre = dict()
        self.trenutna_igra = None
        self.ime_igralca = ime_igralca
        self.igralci_v_sobi = [ime_igralca] + random.sample(imena, stevilo_racunalnikov)
        self.slike_igralcev = {igralec: random.choice(seznam_slik_igralcev) for igralec in self.igralci_v_sobi}
        self.igralci_za_mizo = [igralec for igralec in self.igralci_v_sobi]
        self.big_blind = 10
        self.small_blind = 5
        self.pozicija_big_blind = 2 % len(self.igralci_za_mizo)
        self.pozicija_small_blind = 1 % len(self.igralci_za_mizo)
        self.denar = {igralec: zacetni_denar for igralec in self.igralci_v_sobi}
        self.izid = True

    def izvedi_nujne_stave(self):
        self.trenutna_igra.denar[self.trenutna_igra.igralci[self.pozicija_big_blind]] -= self.big_blind
        self.trenutna_igra.denar[self.trenutna_igra.igralci[self.pozicija_small_blind]] -= self.small_blind
        self.trenutna_igra.stava[self.trenutna_igra.igralci[self.pozicija_big_blind]] = self.big_blind
        self.trenutna_igra.stava[self.trenutna_igra.igralci[self.pozicija_small_blind]] = self.small_blind

    def nova_igra(self, denar):
        self.denar = denar
        self.odstrani_igralce()
        self.pozicija_big_blind += 1
        self.pozicija_small_blind += 1
        self.pozicija_big_blind = self.pozicija_big_blind % len(self.igralci_za_mizo)
        self.pozicija_small_blind = self.pozicija_small_blind % len(self.igralci_za_mizo)

    def odstrani_igralce(self):
        'Igralce, ki nimajo več denarja, odstrani od mize, še vedno pa ostanejo v sobi.'
        #Presteje tiste, ki izpadejo
        izpadli = len(self.igralci_za_mizo)
        self.igralci_za_mizo = [igralec for igralec in self.igralci_za_mizo if self.denar[igralec] > 0]
        izpadli -= len(self.igralci_za_mizo)
        self.big_blind *= 2 ** izpadli
        self.small_blind *= 2 ** izpadli
    
    def preveri_izid(self):
        'Preveri, če igralec ni preživel igre.'
        if self.ime_igralca in self.igralci_za_mizo:
            return False
        return True

class Igra:

    def __init__(self, igralci, denar):
        #Igra bo definirana tako, da se bo seznam igralcev začel s tistim, ki ima žeton big blind
        self.igralci = igralci
        #Odsek: 0 - preflop, 1 - flop, 2 - turn, 3 - river
        self.odsek = 0
        self.na_potezi = 2 % len(self.igralci)
        #Denar je slovar, kjer so ključi igralci in vrednosti njihov denar
        self.denar = denar
        self.karte_na_mizi = ['Neodprta', 'Neodprta', 'Neodprta', 'Neodprta', 'Neodprta']
        self.karte_igralcev = dict()
        self.igralci_v_igri = [igralec for igralec in self.igralci]
        self.kup = nov_kup()
        self.stava = {igralec: 0 for igralec in self.igralci}
        self.konec = False
        self.zmagovalec = None

    def sestej_in_odstrani_stave(self):
        'Sešteje in odstrani vse stave.'
        vsota = 0
        for igralec in self.igralci:
            vsota += self.stava[igralec]
            self.stava[igralec] = 0
        return vsota
    
    def min_stava(self):
        return max([self.stava[igralec] for igralec in self.igralci_v_igri])

    def igralec_folda(self, igralec):
        'Odstrani igralca iz trenutne igre.'
        self.igralci_v_igri.remove(igralec)
    
    def stevilo_igralcev_v_igri(self):
        'Vrne število igralcev v trenutni igri.'
        return len(self.igralci_v_igri)
    
    def igralec_visa_za(self, igralec, vsota):
        'Igralcu poveča stavo in zmanjša denar.'
        #Igralec poveca svojo stavo na podano vsoto
        self.denar[igralec] -= vsota
        self.stava[igralec] += vsota
    
    def igralec_izenaci(self, igralec):
        'Igralcu poveča stavo na najvišjo na mizi.'
        self.denar[igralec] -= self.min_stava() - self.stava[igralec]
        self.stava[igralec] = self.min_stava()
    
    def ime_osebe_na_potezi(self):
        'Vrne ime osebe, ki je trenutno na potezi.'
        return self.igralci[self.na_potezi]
    
    def premakni_potezo(self):
        'Premakne potezo na naslednjega igralca v igri. Pri tem mogoče začne nov odsek igre in zato odpre dodatne karte.'
        
        if self.igralci[self.na_potezi] == self.igralci_v_igri[-1]:
            if self.vse_stave_enake():
                self.odsek += 1
                self.odpri_dodatne_karte()
                self.na_potezi = self.igralci.index(self.igralci_v_igri[0])
            else:
                self.na_potezi = self.igralci.index(self.igralci_v_igri[0])
        else:
            self.na_potezi += 1
            self.na_potezi = self.na_potezi % len(self.igralci)
            while self.igralci[self.na_potezi] not in self.igralci_v_igri:
                self.na_potezi += 1
                self.na_potezi = self.na_potezi % len(self.igralci)
    
    def preveri_zmaga(self):
        'Preveri, ali je mogoče v igri samo en igralec ali pa je konec igre.'
        if self.stevilo_igralcev_v_igri() == 1:
            kandidat = 0
            while self.igralci[kandidat] not in self.igralci_v_igri:
                kandidat += 1
            self.konec = True
            self.zmagovalec = self.igralci[kandidat]
            self.denar[self.zmagovalec] += self.sestej_in_odstrani_stave()
        elif self.odsek == 3 and self.vse_stave_enake() and self.igralci[self.na_potezi] == self.igralci_v_igri[-1]:
            self.konec = True
            self.zmagovalec = self.poisci_zmagovalca()
            self.denar[self.zmagovalec] += self.sestej_in_odstrani_stave()

    def poisci_zmagovalca(self):
        karte_na_mizi = self.karte_na_mizi
        rezultati = {
            igralec: vrednost_sedmerice(karte_na_mizi + self.karte_igralcev[igralec]) for igralec in self.igralci if igralec in self.igralci_v_igri
        }
        najboljse_karte = [0, 0, 0]
        najboljsi_igralec = None
        for igralec in rezultati:
            if rezultati[igralec] > najboljse_karte:
                najboljse_karte = rezultati[igralec]
                najboljsi_igralec = igralec
        return najboljsi_igralec

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
        for igralec in self.igralci_v_igri:
            if not self.stava[self.igralci_v_igri[0]] == self.stava[igralec]:
                return False
        return True