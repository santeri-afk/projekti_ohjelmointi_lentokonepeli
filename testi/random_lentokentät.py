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





hakemus = lentokenttät_random_10()
print(hakemus)