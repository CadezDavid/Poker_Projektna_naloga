from funkcije import *
import bottle

class Poker:

    def __init__(self):
        self.igre = list()

    def dodaj_igro(self):
        self.igre.append(max(self.igre) + 1)
        return max(self.igre)


class Igra:

    def __init__(self, ime, id_igralca, big_blind=10, small_blind=5, stevilo_racunalnikov=2, geslo=None):
        self.ime = ime
        self.stevilo_racunalnikov = stevilo_racunalnikov
        self.geslo = geslo
        self.stevilo_igralcev = 1 + stevilo_racunalnikov
        self.igralci = [id_igralca]
        self.stevilo_igralcev = len(self.igralci)
        self.kup = nov_kup()
        self.big_blind = big_blind
        self.small_blind = small_blind
        self.pozicija_big_blind = 2 % self.stevilo_igralcev
        self.pozicija_small_blind = 1 % self.stevilo_igralcev
        self.minimalno_na_mizi = big_blind
        #Odsek: 0 - preflop, 1 - flop, 2 - turn, 3 - river
        self.odsek = 0
        #Kdo je na potezi, posamezen odsek začne igralec z žetonom big blind
        self.na_potezi = self.pozicija_big_blind
        self.karte_na_mizi = list()
        self.karte_igralcev = dict()
        self.igralci_v_igri = list()
    
    def dodaj_igralca(self, id_igralca):
        self.igralci.append(id_igralca)
        self.stevilo_igralcev += 1
    
    def odstrani_igralca(self, id_igralca):
        novi_igralci = list()
        for igralec in self.igralci:
            if igralec != id_igralca:
                novi_igralci.append(igralec)
        self.igralci = novi_igralci
        self.stevilo_igralcev -= 1
        if self.stevilo_igralcev == 1:
            self.konec_igre()
        self.big_blind *= 2
        self.small_blind *= 2
    
    def razdeli_karte(self):
        for igralec in self.igralci:
            self.karte_igralcev[igralec] = [self.kup.pop() for _ in range(2)]

    def flop(self):
        self.karte_na_mizi += [self.kup.pop() for _ in range(3)]
    
    def turn(self):
        self.karte_na_mizi += [self.kup.pop()]
    
    def river(self):
        self.karte_na_mizi += [self.kup.pop()]

    def nov_krog(self, zmagovalec):
        vsota_stav = 0
        for igralec in self.igralci:
            vsota_stav += igralec.stava
            igralec.stava = 0
        zmagovalec.denar += vsota_stav
        for igralec in self.igralci:
            if igralec.denar == 0:
                self.odstrani_igralca(igralec)
        self.karte_na_mizi = list()
        self.karte_igralcev = list()
        self.kup = nov_kup()
        self.pozicija_big_blind += 1
        self.pozicija_small_blind += 1
        self.pozicija_big_blind = self.pozicija_big_blind % self.stevilo_igralcev
        self.pozicija_small_blind = self.pozicija_small_blind % self.stevilo_igralcev
        self.odsek = 0

    def korak(self):
        if len(self.igralci_v_igri) == 1:
            self.nov_krog(self.igralci_v_igri[0])
        elif self.odsek == 3:
            self.nov_krog(self.poisci_zmagovalca())
        elif all([self.igralci_v_igri[0].stava == igralec.stava for igralec in self.igralci_v_igri[1:]]):
            self.odsek += 1
    
    def poteza(self):
        self.na_potezi += 1
        self.na_potezi = self.na_potezi % self.stevilo_igralcev
    
    def poisci_zmagovalca(self):
        najboljsi = [0, 0, 0]
        zmagovalec = None
        for igralec in self.igralci_v_igri:
            igralceve_karte = vrednost(self.karte_igralcev[igralec] + self.karte_na_mizi)
            if najboljsi < igralceve_karte:
                zmagovalec = igralec
        return zmagovalec
    
    def konec_igre(self):
        return 'Konec igre.'


class Igralec:

    def __init__(self, ime, denar):
        self.denar = denar
        self.v_igri = False
        self.ime = ime
        self.stava = 0
        self.all_in = False
    
    def raising(self, vsota):
        if vsota > self.denar:
            self.stava += vsota
            self.denar -= vsota
        else:
            self.all_in = (True, self.denar)
            self.stava += self.denar
            self.denar = 0
    
    def fold(self):
        self.v_igri = False