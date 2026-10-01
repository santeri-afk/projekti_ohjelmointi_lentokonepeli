import math
import random
import mysql.connector
from geopy.distance import geodesic

YHTEYS_TIEDOT = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "flight_game",
    "user": "root",
    "password": "123#edcvBnmko=9",
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

    return tunnukset

def nayta_tilanne(sijainti, raha, polttoaine):
    print("\n--- PELAAJAN TILANNE ---")
    print("Sijainti:", sijainti)
    print("Raha:", raha, "€")
    print("Polttoaine:", polttoaine, "km")
    print("------------------------")

def etaisyys_km(yhteys, maa1, maa2):
    tulos1 = (hae_kentta_tiedot(yhteys, maa1)["latitude_deg"], hae_kentta_tiedot(yhteys, maa1)["longitude_deg"])

    tulos2 = (hae_kentta_tiedot(yhteys, maa2)["latitude_deg"], hae_kentta_tiedot(yhteys, maa2)["longitude_deg"])
    return (geodesic(tulos1, tulos2).km)

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

if __name__ == "__main__":

    yhteys = avaa_yhteys()
    nykyinen_sijainti = KOTIKENTTA
    raha = 0
    polttoaine = ALKU_POLTTOAINE
    
    tunnukset = lentokentat_random_10(yhteys)
    tunnukset = [KOTIKENTTA] + tunnukset[:9]

    while True:
        
        nayta_tilanne(nykyinen_sijainti, raha, polttoaine)

        print("")
        print("Lentokentät etäisyyksineen sijainnista", nykyinen_sijainti, ":")
        tulosta_kentat(yhteys, nykyinen_sijainti, tunnukset)

        print("0. Lopeta")
        valinta = input("Valintasi: ")

        if valinta == "0":
            print("Peli lopetettu.")
            break
        #EN TIEDÄ MITÄ TEKEE MUTTA PITI OLLA MUUTEN HEITTI ERROR JOS VÄÄRÄ MERKKI
        #tai siis en tiedä isdigit yms
        if valinta.isdigit() and 1 <= int(valinta) <= len(tunnukset):
            indeksi = int(valinta) - 1
            polttoaine -= etaisyys_km(yhteys, nykyinen_sijainti, tunnukset[indeksi])
            polttoaine = round(polttoaine)
            if polttoaine < 0:
                print("Hävisit pelin.")
                break
            nykyinen_sijainti = tunnukset[indeksi]
        else:
            print("VÄÄRÄ VALINTA")
        #____________________________________________________________
    yhteys.close()