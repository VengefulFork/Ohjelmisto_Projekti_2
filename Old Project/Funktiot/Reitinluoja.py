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
    # Käydään läpi sql haun palauttama lista joka sisältää monikon ja määritellään aloitus_kenttä täksi monikoksi
    for i in aloitus_kenttä :
        aloitus_kenttä = i

    curs.execute(sql_lopetus)
    lopetus_kenttä = curs.fetchall()


    testaus = True
    while testaus :
        # Haetaan aloituskentällä olevat yhteydet
        sql_testaus1 = f"SELECT lopetuspiste FROM airport, yhteys WHERE airport.ident = yhteys.aloituspiste AND ident = '{aloitus_kenttä[1]}'"
        sql_testaus2 = f"SELECT aloituspiste FROM airport, yhteys WHERE airport.ident = yhteys.lopetuspiste AND ident = '{aloitus_kenttä[1]}'"
        curs.execute(sql_testaus1)
        testaus_yhteydet = curs.fetchall()
        curs.execute(sql_testaus2)
        testaus_yhteydet.extend(curs.fetchall())

        # Käydään läpi kaikki aloitus kentällä olevat yhteydet
        for i in testaus_yhteydet :
            # Jos aloitus kenttältä on yhteys lopetus kentälle arvotaan uusi aloitus kenttä tai jos ne ovat sama kenttä arvotaan uusi kenttä
            if lopetus_kenttä[0][1] in i or aloitus_kenttä[1] == lopetus_kenttä[0][1] :

                sql = f"SELECT name, ident FROM airport WHERE ident ='{kentät_icao[random.randint(0, 20)]}'"
                curs.execute(sql)
                aloitus_kenttä = curs.fetchall()
                # Käydään läpi sql haun palauttama lista joka sisältää monikon ja määritellään aloitus_kenttä täksi monikoksi
                for a in aloitus_kenttä :
                    aloitus_kenttä = a

                break
            # Jos lopetus kenttä ei ole aloitus kentän yhteyksissä rikotaan silmukka
            if lopetus_kenttä[0][1] not in i :

                testaus = False
        continue

    return aloitus_kenttä , lopetus_kenttä

