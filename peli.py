import math
import random
import mysql.connector
from geopy.distance import geodesic

###############################
# Laita oma user ja salasana  #
###############################
YHTEYS_TIEDOT = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "flight_game",
    "user": "KÄYTTÄJÄSI",
    "password": "SALASANASI",
    "autocommit": True,
    "collation": "utf8mb4_general_ci",
}

KOTIKENTTA = "EFHK"        # Helsinki-Vantaa
KENTTIEN_MAARA = 9         # montako kohdekenttaa arvotaan peliin
TAVOITE_RAHA = 400         # paljonko rahaa pitaa kerata voittaakseen
ALKU_POLTTOAINE = 9000     # kilometreina


def avaa_yhteys():
    """Avaa yhteyden tietokantaan ja palauttaa yhteysolion."""
    return mysql.connector.connect(**YHTEYS_TIEDOT)

###################################
#      Rahanrandomisointi         #
###################################
def anna_rahaa_uudesta_kentasta(kohde, kaydyt_kentat, raha):
    if kohde not in kaydyt_kentat:
        saatu_raha = random.randint(65, 125)
        raha += saatu_raha
        kaydyt_kentat.add(kohde)

        print("Uusi lentokenttä!")
        print("Sait rahaa:", saatu_raha, "€")

    else:
        print("Olet jo käynyt tällä lentokentällä.")
        print("Et saanut rahaa.")

    return raha  

#######################################################
#     Hakee tietokannasta kenttien tiedot identillä   #
#######################################################
def hae_kentta_tiedot(yhteys, ident):
    """Hakee yhden lentokentan ICAO-tunnuksen perusteella."""
    kursori = yhteys.cursor(dictionary=True)
    sql = """SELECT ident, name, municipality, iso_country,
                    latitude_deg, longitude_deg
             FROM airport
             WHERE ident = %s"""
    kursori.execute(sql, (ident,))
    rivi = kursori.fetchone()
    kursori.close()
    return rivi

######################################################
#      Hakee kymmenen random kentän identit          #
######################################################
def lentokentat_random_10(yhteys):
    kursori = yhteys.cursor()
    sql = """SELECT ident FROM airport
             WHERE continent = 'EU' AND type = 'large_airport'
             ORDER BY RAND() LIMIT 10"""
    kursori.execute(sql)
    tulos = kursori.fetchall()
    kursori.close()

    tunnukset = []
    for rivi in tulos:
        tunnukset.append(rivi[0])
        if len(tunnukset) == KENTTIEN_MAARA:
            return tunnukset

##########################################################
#     Näyttää sijainnin rahat yms roundien välissä       #
##########################################################
def nayta_tilanne(nimi, sijainti, raha, polttoaine):
    print("\n--- PELAAJAN TILANNE ---")
    print("Pelaaja:", nimi)
    print("Sijainti:", sijainti)
    print("Raha:", raha, "€")
    print("Polttoaine:", polttoaine, "km")
    print("------------------------")

##############################################
#        laskee a ja b kentän etäisyyden     #
##############################################
def etaisyys_km(yhteys, maa1, maa2):
    tulos1 = (hae_kentta_tiedot(yhteys, maa1)["latitude_deg"], hae_kentta_tiedot(yhteys, maa1)["longitude_deg"])

    tulos2 = (hae_kentta_tiedot(yhteys, maa2)["latitude_deg"], hae_kentta_tiedot(yhteys, maa2)["longitude_deg"])
    return (geodesic(tulos1, tulos2).km)

########################################
#     Tulostaa kentät listaksi         #
########################################
def tulosta_kentat(yhteys, oma_sijainti, tunnukset):
    numero = 1
    for tunnus in tunnukset:
        kentta = hae_kentta_tiedot(yhteys, tunnus)
        matka = etaisyys_km(yhteys, oma_sijainti, tunnus)
        print(numero, ".", kentta["name"],
              "(" + kentta["ident"] + ")",
              "-", kentta["municipality"],
              "-", round(matka), "km")
        numero = numero + 1

########################################
#       pelin aloitus ohjeet yms       #
########################################
def pelinaloitus():
    print("\n==============================")
    print("        LENTOPELI")
    print("==============================")
    print("\nTervetuloa")
    print(f"\nLähdet matkalle Helsinki-Vantaalta ({KOTIKENTTA}) ympäri Eurooppaa.")
    print("\nTEHTÄVÄSI:")
    print(f"  - Kerää yhteensä {TAVOITE_RAHA} € lentämällä kentältä toiselle.")
    print(f"  - Polttoainetta on {ALKU_POLTTOAINE} km verran. Jokainen lento kuluttaa sitä.")
    print(f"  - Palaa lopuksi takaisin Helsinkiin ({KOTIKENTTA}).")
    print("\nVAROITUS:")
    print("  Jos polttoaine loppuu kesken matkan, peli on hävitty.")
    print("  Suunnittele reittisi siis tarkasti!")
    print("\nHyvää lentoa!\n")

##############
#   Peli     #
##############
if __name__ == "__main__":

    yhteys = avaa_yhteys()

    while True:
        pelinaloitus()
        pelaajan_nimi = input("Anna pelaajan nimi: ")
        nykyinen_sijainti = KOTIKENTTA
        raha = 0
        polttoaine = ALKU_POLTTOAINE
        kaydyt_kentat = set()
        tunnukset = lentokentat_random_10(yhteys)
        tunnukset = [KOTIKENTTA] + tunnukset[:9]

        while True:
            
            nayta_tilanne(pelaajan_nimi, nykyinen_sijainti, raha, polttoaine)

            print("")
            print("Lentokentät etäisyyksineen sijainnista", nykyinen_sijainti, ":")
            tulosta_kentat(yhteys, nykyinen_sijainti, tunnukset)

            print("0. Lopeta")
            valinta = input("Valintasi: ")

            if valinta == "0":
                print("Peli lopetettu.")
                break
            if valinta.isdigit() and 1 <= int(valinta) <= len(tunnukset):
                indeksi = int(valinta) - 1
                polttoaine -= etaisyys_km(yhteys, nykyinen_sijainti, tunnukset[indeksi])
                polttoaine = round(polttoaine)
                if polttoaine < 0:
                    print("Hävisit pelin.")
                    break
                nykyinen_sijainti = tunnukset[indeksi]

                if nykyinen_sijainti == KOTIKENTTA:
                    if raha < TAVOITE_RAHA:
                        print("Ei ollut tarpeeksi rahaa. Hävisit pelin.")
                        break
                    else:
                        print("Voitit pelin.")
                        break
                else:
                    raha = anna_rahaa_uudesta_kentasta(nykyinen_sijainti, kaydyt_kentat, raha)
            else:
                print("VÄÄRÄ VALINTA")
            
        uudestaan = int(input("Haluatko pelaa uudestaan? laita 0 että peli lopettaa tai laita 1 jos haluat pelata uudestaan: "))
        if uudestaan == 1:
            continue
        else:
            break
    yhteys.close()