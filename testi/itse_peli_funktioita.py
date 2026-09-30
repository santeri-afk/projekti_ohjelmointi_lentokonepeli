from tilanne import nayta_tilanne
from hae_kentan_tiedot_fun import hae_kentta_tiedot
from maiden_pituus import maiden_pituus
from random_lentokentat import lentokenttät_random_10 
def peli():
    raha = 0
    polttoaine = 9000
    sijainti = "EFHK"

    nayta_tilanne(sijainti, raha, polttoaine)
    peli()