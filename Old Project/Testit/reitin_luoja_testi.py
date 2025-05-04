import mariadb
import random

yhteys = mariadb.connect(
        host='localhost',
        port= 3306,
        database= 'peli_projekti',
        user= 'player',
        password= '12345',
        autocommit=True
)


def reitinluoja ():
    kentät_icao = ("EFHK", "EFKT", "ESSA", "ENGM", "ENTC", "BIKF", "EGPD", "EGLL", "LFPG", "LEMD",
                   "LIRF", "LSZH", "EDDB", "EPWA", "EKBI", "EVRA", "LOWW", "LRBS", "LQSA", "LGAV", "EHAM")
    # RNG aloitus ja lopetus kenttien arpomista varten.
    aloitus_kenttä = kentät_icao[random.randint(0, 20)]
    lopetus_kenttä = kentät_icao[random.randint(0, 20)]
    # Testataan ovatko aloitus_kenttä ja lopetus_kenttä samat ja jos on niin arvotaan uusi lopetus_kenttä
    if aloitus_kenttä == lopetus_kenttä :
        lopetus_kenttä = kentät_icao[random.randint(0, 20)]
    # sql haut
    sql_aloitus = f"SELECT name, ident FROM airport WHERE ident = '{aloitus_kenttä}'"
    sql_lopetus = f"SELECT name, ident FROM airport WHERE ident = '{lopetus_kenttä}'"

    curs = yhteys.cursor()

    curs.execute(sql_aloitus)
    aloitus_kenttä = curs.fetchall()
    for i in aloitus_kenttä :
        aloitus_kenttä = i

    curs.execute(sql_lopetus)
    lopetus_kenttä = curs.fetchall()
    # Testausta varten
    # for i in aloitus_kenttä :
    #     print(f"Pelaaja aloitus kenttäsi on {i[0]}")
    # for a in lopetus_kenttä :
    #     print(f"Ja Maalisi on {a[0]}. \nOnnea matkaan")

    testaus = True
    while testaus :
        sql_testaus1 = f"SELECT lopetuspiste FROM airport, yhteys WHERE airport.ident = yhteys.aloituspiste AND ident = '{aloitus_kenttä[1]}'"
        sql_testaus2 = f"SELECT aloituspiste FROM airport, yhteys WHERE airport.ident = yhteys.lopetuspiste AND ident = '{aloitus_kenttä[1]}'"
        curs.execute(sql_testaus1)
        testaus_yhteydet = curs.fetchall()
        curs.execute(sql_testaus2)
        testaus_yhteydet.extend(curs.fetchall())
        # print(testaus_yhteydet)
        # print(aloitus_kenttä)
        # print(lopetus_kenttä)

        for i in testaus_yhteydet :
            if lopetus_kenttä[0][1] in i or aloitus_kenttä[1] == lopetus_kenttä[0][1] :
                print("Löytyi")
                sql = f"SELECT name, ident FROM airport WHERE ident ='{kentät_icao[random.randint(0, 20)]}'"
                curs.execute(sql)
                aloitus_kenttä = curs.fetchall()
                for a in aloitus_kenttä :
                    aloitus_kenttä = a
                # print(aloitus_kenttä)
                break
            if lopetus_kenttä[0][1] not in i :
                print("Ei löytynyt")
                testaus = False
        continue

    print(lopetus_kenttä[0][1])
    return aloitus_kenttä , lopetus_kenttä

reitinluoja()
