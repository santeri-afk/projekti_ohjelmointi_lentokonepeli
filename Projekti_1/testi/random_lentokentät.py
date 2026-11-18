import mysql.connector

def lentokenttat_random_10():
    lentokentat_random = []
    sql =f"Select name, ident from airport where continent = 'EU' and type = 'Large_airport' order by rand() LIMIT 10"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount > 0:
        for kursori in tulos:
            lentokentat_random.append(kursori)

    return lentokentat_random 


yhteys = mysql.connector.connect(
    host="127.0.0.1",
    port= 3306,
    database="flight_game",
    user="root",
    #en laita salasanaa näkyvillä koska se on public reposity
    password="123#edcvBnmko=9",
    autocommit=True
    )



hakemus = lentokenttat_random_10()
print(hakemus)