from geopy import distance
import mysql.connector


def lentokentien_matka(kenttä1, kenttä2):
    laskuri = 1
    sql =f"Select latitude_deg, longitude_deg from airport where ident='{kenttä1}' or ident='{kenttä2}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount > 0:
        print("hakemallassi lentokentillä on näin kaukana toisistaan")
        for kursori in tulos:
            
            if laskuri == 1:
                a = kursori
                laskuri += 1
            elif laskuri == 2:
                b = kursori
                dist = distance.distance(a, b).km
                dist_rounded = round(dist, 2)
                print(f"{dist_rounded} km")




yhteys = mysql.connector.connect(
    host="127.0.0.1",
    port= 3306,
    database="ohjelmointi_projekti_flight",
    user="root",
    password="******",
    autocommit=True
    )