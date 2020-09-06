import poker
import random
import funkcije


def verjetnost_zmage(karte_na_mizi, karte):
    'Naključno bo odigral 1000 iger in pogledal, kolikokrat zmaga s svojimi kartami.'
    if karte_na_mizi == list():
        karte_na_mizi = funkcije.nov_kup_brez(karte)[:5]
    stevilo_zmag = 0
    vrednost_kart = funkcije.vrednost_sedmerice(karte_na_mizi + karte)
    for _ in range(1000):
        karte_nasprotnika = [funkcije.nov_kup_brez(karte).pop() for _ in range(2)]
        if funkcije.vrednost_sedmerice(karte_nasprotnika + karte_na_mizi) < vrednost_kart:
            stevilo_zmag += 1
    return stevilo_zmag / 1000

def verjetnost_zmage_prvi_odsek(karte):
    'Enako kot verjetnost_zmage, ampak tu še ni kart na mizi, zato si izbere svoje, naključne.'
    stevilo_zmag = 0
    for _ in range(10):
        karte_na_mizi = [funkcije.nakljucna_karta_not_in_karte(karte) for _ in range(3)]
        vrednost_kart = funkcije.vrednost_sedmerice(karte_na_mizi + karte)
        for _ in range(100):
            karte_nasprotnika = [funkcije.nakljucna_karta_not_in_karte(karte + karte_na_mizi) for _ in range(2)]
            if funkcije.vrednost_sedmerice(karte_nasprotnika + karte_na_mizi) < vrednost_kart:
                stevilo_zmag += 1
    return stevilo_zmag / (10 * 100)


def izvedi_smiselno_potezo(igra, igralec, drznost):
    karte_na_mizi = funkcije.preciscene_karte(igra.karte_igralcev[igralec])
    
    if igra.odsek == 0:
        verjetnost = verjetnost_zmage_prvi_odsek(igra.karte_igralcev[igralec]) + 0.3
    else:
        verjetnost = verjetnost_zmage(karte_na_mizi, igra.karte_igralcev[igralec])

    if random.random() < verjetnost + drznost ** 0.2:
        
        pogoj1 = int(random.random() < verjetnost)
        pogoj2 = int(random.random() < drznost)
        pogoj3 = int(igra.zaporedni_krog == 0)
        pogoj4 = int(igra.min_stava() > igra.stava[igralec])
        if igra.denar[igralec] + igra.stava[igralec] < igra.min_stava():
            igra.all_in(igralec)
        elif pogoj1 * pogoj2 * (pogoj3 + pogoj4):
            denar = igra.denar[igralec]
            delez_ki_ga_bo_stavil = random.choice([0.02] * 16 + [0.08] * 20 + [0.15] * 5 + [drznost] * 6)
            stava = denar * delez_ki_ga_bo_stavil
            stava = int(stava - stava % 5)
            igra.igralec_visa_za(igralec, max(igra.min_stava(), stava))
        else:
            igra.igralec_izenaci(igralec)
    
    else:
        igra.igralec_folda(igralec)