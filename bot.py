import poker
import random

def izvedi_nakljucno_potezo(igra, igralec):
    if random.choice([False, True, True]):
        igra.stava[igralec] = max(list(igra.stava.values()))
    elif random.choice([False, True]):
        igra.igralci_v_igri[igralec] = False
    else:
        igra.stava[igralec] = max(list(igra.stava.values())) + 10