import poker
import random

def izvedi_nakljucno_potezo(igra, igralec):
    if igra.odsek == 0:
        if random.choice([False, True]):
            igra.igralec_izenaci(igralec)
        elif random.choice([False, False, False, False, True]):
            igra.igralec_folda(igralec)
        else:
            igra.igralec_visa_za(igralec, random.choice([10, 20, 50]))
    else:
        if random.choice([False, True]):
            igra.igralec_izenaci(igralec)
        elif random.choice([False, False, False, True]):
            igra.igralec_folda(igralec)
        else:
            igra.igralec_visa_za(igralec, random.choice([10, 20, 50]))