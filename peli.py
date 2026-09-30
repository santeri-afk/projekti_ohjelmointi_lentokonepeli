import math
import random
import mysql.connector
# laita konsoliin/terminaaliin "pip install mysql-connector-python" jos mysql.connector import ei meinaa toimia
# ASETUKSET - muuta user ja password sopiviksi sinulle
#____________________________________________________
YHTEYS_TIEDOT = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "flight_game",
    "user": "root",
    "password": "root",
    "autocommit": True,
    "collation": "utf8mb4_general_ci",
}
#_____________________________________________________


#avaa yhteyden sql
def avaa_yhteys():
    return mysql.connector.connect(**YHTEYS_TIEDOT)


KOTIKENTTA = "EFHK"        # Helsinki-Vantaa
KENTTIEN_MAARA = 9         # montako kohdekenttaa arvotaan peliin
TAVOITE_RAHA = 400        # paljonko rahaa pitaa kerata voittaakseen
ALKU_POLTTOAINE = 9000     # kilometreina


#tarvitaan ainakin funktiot: kentän haku/ kenttien valitseminen x määrä isoja kenttiä euroopasta
#funkitoi joka lasekee kenttien etäisyyden
#funktio joka kertoo pelaajan sijainnit ja muut tiedot valintojen välissä
#tulostaa vaihotehdot minne lentää ja kysyy
#itse peli käyttämällä avuksi funktioita