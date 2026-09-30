
def hae_kentta_tiedot(yhteys, ident):
    #Hakee yhden lentokentan ICAO-tunnuksen perusteella.
    kursori = yhteys.cursor(dictionary=True)
    sql = """SELECT ident, name, municipality, iso_country,
                    latitude_deg, longitude_deg
             FROM airport
             WHERE ident = %s"""
    kursori.execute(sql, (ident,))
    rivi = kursori.fetchone()
    kursori.close()
    return rivi
# tällä kun laittaa esim frankvurtin icao koodin kertoo oleelliset tiedot kordinaatit yms
tulos = hae_kentta(yhteys, "EDDF")

print(tulos)