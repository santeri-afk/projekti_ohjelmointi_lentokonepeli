import mysql.connector

def lentokenttät_random_10():
    lentokentät_random = []
    sql =f"Select ident from airport where continent = 'EU' and type = 'Large_airport' order by rand() LIMIT 10"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount > 0:
        for kursori in tulos:
            lentokentät_random.append(kursori)

    return lentokentät_random 


yhteys = mysql.connector.connect(
    host="127.0.0.1",
    port= 3306,
    database="flight_game",
    user="root",
    #en laita salasanaa näkyvillä koska se on public reposity
    password="1234",
    autocommit=True
    )



hakemus = lentokenttät_random_10()
print(hakemus)