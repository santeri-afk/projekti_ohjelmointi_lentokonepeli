import math
import random
import mysql.connector
from geopy.distance import geodesic
from flask import Flask, request, render_template, url_for, redirect
import sys

###############################
# Laita oma user ja salasana  #
###############################
YHTEYS_TIEDOT = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "flight_game",
    "user": "jere1",
    "password": "abc123",
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



##############################################
#        laskee a ja b kentän etäisyyden     #
##############################################
def etaisyys_km(yhteys, maa1, maa2):
    tulos1 = (hae_kentta_tiedot(yhteys, maa1)["latitude_deg"], hae_kentta_tiedot(yhteys, maa1)["longitude_deg"])

    tulos2 = (hae_kentta_tiedot(yhteys, maa2)["latitude_deg"], hae_kentta_tiedot(yhteys, maa2)["longitude_deg"])
    return (geodesic(tulos1, tulos2).km)

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


def nayta_tilanne2(nimi, sijainti, raha, polttoaine):
    teksti = "<link rel='stylesheet' href='/static/peli.css'><p>--- PELAAJAN TILANNE ---</p>"
    teksti += f"<p>Pelaaja: {nimi}</p>"
    teksti += f"<p>Sijainti: {sijainti}</p>"
    teksti += f"<p>Raha: {raha}€</p>"
    teksti += f"<p>Polttoaine: {polttoaine}</p>"
    teksti += f"<form method='POST' action='/peli'><input name='text' style='display: none'><input type='submit' style='display: none'> <a href='/uudelleen'>Aloita uudelleen</a>"
    return teksti

def tulosta_kentat2(yhteys, oma_sijainti, tunnukset):
    palautus = "<form method='POST'>"
    numero = 1
    for tunnus in tunnukset:
        kentta = hae_kentta_tiedot(yhteys, tunnus)
        matka = etaisyys_km(yhteys, oma_sijainti, tunnus)
        palautus += f"<p>{str(numero)}. {kentta["name"]}</p> <p>({kentta["ident"]})</p> <p>-{kentta["municipality"]}-</p> <p>{round(matka)}km</p> <input type='submit' value='{numero}' name='v'/>"
        numero = numero + 1
    palautus += "</form>"
    return palautus


app = Flask(__name__)
@app.route('/')
def my_form():
    return render_template('peli.html')


@app.route('/', methods=['POST'])
def my_form_post():
    global yhteys, nykyinen_sijainti, tunnukset, pelaajan_nimi, raha, kaydyt_kentat, polttoaine
    yhteys = avaa_yhteys()
    pelinaloitus()
    pelaajan_nimi = request.form['text'].upper()

    nykyinen_sijainti = KOTIKENTTA
    raha = 0
    polttoaine = ALKU_POLTTOAINE
    kaydyt_kentat = set()
    tunnukset = lentokentat_random_10(yhteys)
    tunnukset = [KOTIKENTTA] + tunnukset[:9]

    try:
        valinta = int(request.form['text'].upper()) - 1
        polttoaine -= round(etaisyys_km(yhteys, nykyinen_sijainti, tunnukset[valinta]))
        nykyinen_sijainti = tunnukset[valinta]
        raha = anna_rahaa_uudesta_kentasta(nykyinen_sijainti, kaydyt_kentat, raha)
    except ValueError:
        pass

    tilanne = ""
    tilanne += nayta_tilanne2(pelaajan_nimi, nykyinen_sijainti, raha, polttoaine)
    tilanne += tulosta_kentat2(yhteys, nykyinen_sijainti, tunnukset)
    return tilanne


@app.route('/peli', methods=['POST'])
def peli():
    global yhteys, nykyinen_sijainti, tunnukset, pelaajan_nimi, raha, kaydyt_kentat, polttoaine
    try:
        pelaajan_nimi
    except NameError:
        return redirect(url_for("my_form"))

    valinta = request.form['v'].upper()
    if valinta.isdigit() and 1 <= int(valinta) <= len(tunnukset):
        valinta = int(valinta)-1
        polttoaine -= round(etaisyys_km(yhteys, nykyinen_sijainti, tunnukset[valinta]))
        if (polttoaine < 0):
            return redirect(url_for("havio"))
        nykyinen_sijainti = tunnukset[valinta]
        if (nykyinen_sijainti == KOTIKENTTA):
            if (raha < TAVOITE_RAHA):
                return redirect(url_for("havio"))
            else:
                return redirect(url_for("voitto"))
        raha = anna_rahaa_uudesta_kentasta(nykyinen_sijainti, kaydyt_kentat, raha)

    tilanne = ""
    tilanne += nayta_tilanne2(pelaajan_nimi, nykyinen_sijainti, raha, polttoaine)
    tilanne += tulosta_kentat2(yhteys, nykyinen_sijainti, tunnukset)
    return tilanne


@app.route('/havio', methods=['GET', 'POST'])
def havio():
    global raha
    return f"<link rel='stylesheet' href='/static/loppu.css'><h1>Hävisit pelin</h1><p>Raha:{raha}€</p><a href='/uudelleen'>Aloita uudelleen</a>"
@app.route('/voitto', methods=['GET', 'POST'])
def voitto():
    global raha
    return f"<link rel='stylesheet' href='/static/loppu.css'><h1>Voitit pelin</h1><p>Raha:{raha}€</p><a href='/uudelleen'>Aloita uudelleen</a>"


@app.route('/uudelleen', methods=['GET', 'POST'])
def uudelleen():
    return redirect(url_for("my_form"))



app.run(host="127.0.0.1", port=3000, debug=True)