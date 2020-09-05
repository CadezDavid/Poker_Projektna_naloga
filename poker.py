from funkcije import *
import bottle
import json
import random


class Poker:

    def __init__(self, ime_igralca, stevilo_racunalnikov=3, zacetni_denar=2000):
        with open('imena.txt', 'r') as dat:
            imena = [ime.rstrip() for ime in dat.readlines()]
        self.trenutna_igra = None
        self.ime_igralca = ime_igralca
        self.igralci_v_sobi = [ime_igralca] + random.sample(imena, stevilo_racunalnikov)
        slike = seznam_slik_igralcev
        random.shuffle(slike)
        self.slike_igralcev = {igralec: slike[i] for i, igralec in enumerate(self.igralci_v_sobi)}
        self.igralci_za_mizo = [igralec for igralec in self.igralci_v_sobi]
        self.big_blind = 10
        self.pozicija_big_blind = 2 % len(self.igralci_za_mizo)
        self.denar = {igralec: zacetni_denar for igralec in self.igralci_v_sobi}
        self.izid = True
    
    def pozicija_small_blind(self):
        return (self.pozicija_big_blind - 1) % len(self.igralci_za_mizo)

    def small_blind(self):
        return self.big_blind // 2

    def nova_igra(self, denar):
        self.denar = denar
        self.odstrani_igralce()
        self.pozicija_big_blind += 1
        self.pozicija_big_blind = self.pozicija_big_blind % len(self.igralci_za_mizo)
        big_blind = self.big_blind
        self.trenutna_igra = Igra(self.igralci_za_mizo, denar, self.pozicija_big_blind, big_blind)
    
    def prva_igra(self):
        igralci = self.igralci_za_mizo
        denar = self.denar
        pozicija_big_blind = self.pozicija_big_blind
        big_blind = self.big_blind
        self.trenutna_igra = Igra(igralci, denar, pozicija_big_blind, big_blind)

    def odstrani_igralce(self):
        'Igralce, ki nimajo več denarja, odstrani od mize, še vedno pa ostanejo v sobi.'
        #Presteje tiste, ki izpadejo
        izpadli = len(self.igralci_za_mizo)
        self.igralci_za_mizo = [igralec for igralec in self.igralci_za_mizo if self.denar[igralec] > 0]
        izpadli -= len(self.igralci_za_mizo)
        self.big_blind *= 2 ** izpadli
    
    def preveri_izid(self):
        'Preveri, če igralec ni preživel igre.'
        ni_ga_vec = self.ime_igralca not in self.igralci_za_mizo
        edini_je = self.igralci_za_mizo == [self.ime_igralca]
        return [
            ni_ga_vec or edini_je,
            edini_je
        ]

class Igra:

    def __init__(self, igralci, denar, pozicija_big_blind, big_blind):
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
        self.pozicija_big_blind = pozicija_big_blind
        self.big_blind = big_blind

    def small_blind(self):
        return self.big_blind // 2

    def pozicija_small_blind(self):
        return (self.pozicija_big_blind - 1) % len(self.igralci)

    def igralec_z_big_blind(self):
        return self.igralci[self.pozicija_big_blind]
    
    def igralec_s_small_blind(self):
        return self.igralci[self.pozicija_small_blind()]

    def sestej_in_odstrani_stave(self):
        'Sešteje in odstrani vse stave.'
        vsota = 0
        for igralec in self.igralci:
            vsota += self.stava[igralec]
            self.stava[igralec] = 0
        return vsota
    
    def izvedi_nujne_stave(self):
        poz_bbl = self.pozicija_big_blind
        st_igr = len(self.igralci)
        igralec_z_bbl = self.igralci[poz_bbl]
        igralec_s_sbl = self.igralci[(poz_bbl - 1) % st_igr]
        self.igralec_visa_za(igralec_z_bbl, self.big_blind)
        self.igralec_visa_za(igralec_s_sbl, self.big_blind // 2)
    
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
    
    def all_in(self, igralec):
        self.stava[igralec] += self.denar[igralec]
        self.denar[igralec] = 0
    
    def ime_osebe_na_potezi(self):
        'Vrne ime osebe, ki je trenutno na potezi.'
        return self.igralci[self.na_potezi]
    
    def premakni_potezo(self):
        'Premakne potezo na naslednjega igralca v igri. Pri tem mogoče začne nov odsek igre in zato odpre dodatne karte.'
        self.preveri_zmaga()
        if not self.konec:
            if self.igralci[self.na_potezi] == self.igralec_s_small_blind():
                if self.vse_stave_enake():
                    self.odsek += 1
                    self.odpri_dodatne_karte()
                    self.na_potezi = self.pozicija_big_blind
                else:
                    self.na_potezi = self.pozicija_big_blind
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
        elif self.odsek == 3 and self.vse_stave_enake() and self.igralci[self.na_potezi] == self.igralec_s_small_blind():
            self.konec = True
            self.zmagovalec, self.zmagovalne_karte = self.poisci_zmagovalca()
            if len(self.zmagovalec) == 1:
                self.denar[self.zmagovalec[0]] += self.sestej_in_odstrani_stave()
            else:
                stave = self.sestej_in_odstrani_stave()
                for igralec in self.zmagovalec:
                    self.denar[igralec] += stave // len(self.zmagovalec)

    def poisci_zmagovalca(self):
        karte_na_mizi = self.karte_na_mizi
        karte = {
            igralec: (karte_na_mizi + self.karte_igralcev[igralec]) for igralec in self.igralci_v_igri
        }
        seznam_najboljsih = list()
        for igralec in self.igralci_v_igri:
            if all([primerjaj_sedmerici(karte[igralec], karte[drug]) != 2 for drug in self.igralci_v_igri]):
                seznam_najboljsih.append(igralec)
        return seznam_najboljsih, [vrednost_sedmerice(karte[igralec]) for igralec in seznam_najboljsih]


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
        stave = [self.stava[igralec] for igralec in self.igralci_v_igri]
        return enaki_v_sez(stave)
    
    def zadnji_v_krogu(self):
        'Preveri, če je na poziciji zadnji v nekem krogu.'
