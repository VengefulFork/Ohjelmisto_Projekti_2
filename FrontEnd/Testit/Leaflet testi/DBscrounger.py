import json
import random
import mariadb
from flask import Flask, Response
from flask_cors import CORS

tk_yhteys = mariadb.connect(
    host='localhost',
    port=3306,
    database='peli_projekti',
    user='player',
    password='12345',
    autocommit=True
)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/search/')

def search():
    c = tk_yhteys.cursor()
    db_search = f"SELECT name, ident, latitude_deg, longitude_deg FROM airport"
    c.execute(db_search)
    data = c.fetchall()
    data_list = []
    for a in data :
        r = {
            "Name": a[0],
            "Icao": a[1],
            "Lat": a[2],
            "Long": a[3]

        }
        data_list.append(r)

    json_response = json.dumps(data_list)
    response = Response(response=json_response, status=202, mimetype="application/json")
    response.headers["Content-Type"] = "charset=utf-8"




    return response

@app.route('/creator/')

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

    curs = tk_yhteys.cursor()

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
    response_list = []
    a = {
        "Name" : aloitus_kenttä[0],
        "Icao" : aloitus_kenttä[1],
    }
    response_list.append(a)
    b = {
        "Name" : lopetus_kenttä[0][0],
        "Icao" : lopetus_kenttä[0][1],
    }
    response_list.append(b)

    json_response = json.dumps(response_list)
    response = Response(response=json_response, status=202, mimetype="application/json")
    response.headers["Content-Type"] = "charset=utf-8"
    return response

@app.route('/flying/<playerlocation>/<fieldIcao>')
def lentäminen(playerlocation, fieldIcao):
    # SQL Komentoja varten
    pelaajan_sijainti = playerlocation
    pelaajan_sijainti = pelaajan_sijainti.replace(" ", "")
    valittu_kenttä = fieldIcao
    print(valittu_kenttä)
    curs = tk_yhteys.cursor()


    # Haetaan kaikki lentoyhtydet joita kentällä jolla pelaaja tällä hetkellä on.
    sql = f"SELECT lopetuspiste FROM airport, yhteys WHERE airport.ident = yhteys.aloituspiste AND ident = '{pelaajan_sijainti}'"
    sql2 = f"SELECT aloituspiste FROM airport, yhteys WHERE airport.ident = yhteys.lopetuspiste AND ident = '{pelaajan_sijainti}'"
    curs.execute(sql)
    yhteydet = curs.fetchall()
    curs.execute(sql2)
    yhteydet.extend(curs.fetchall())
    print(yhteydet)

    # Haetaan vielä identia vastaavan kentän nimi pelaajalle
    kentät_nimet = []
    for a in yhteydet :
        curs.execute(f"SELECT name, ident FROM airport WHERE ident = '{a[0]}'")
        kentät_nimet.extend(curs.fetchall())

    # Tulostetaan yhteydet pelaajalle
    print(f"\nOlet kentällä {pelaajan_sijainti}, {pelaajan_sijainti} josta valittavat yhteydet ovat : ")
    for rivi in kentät_nimet :
        print (f"\nKentän nimi on {rivi[0]} ja ICAO-koodi: {rivi[1]}")


    loop = 1

    while loop != 3 :
        # Jos pelaajan antama ICAO koodi on virheellinen tulostetaan uudestaan sijainti ja sieltä olevat kenttä yhteydet
        if loop == 2 :
            print("\nAnnoit Väärän ICAO koodin kokeile uudestaan")
            print(f"\nOlet kentällä {pelaajan_sijainti}, {pelaajan_sijainti} josta valittavat yhteydet ovat : ")
            for rivi in kentät_nimet:
                print(f"\nKentän nimi on {rivi[0]} ja ICAO-koodi: {rivi[1]}")
        #Pyydetään käyttäjältä kenttä jolle haluaa lentää ja poistetaan siitä vielä mahdolliset välilyönnit
        # valittu_kenttä = input("\nAnna kentän ICAO-koodi jolle haluat lentää = ").upper().replace(" ", "")
        # Käydään läpi kaikki monikot jota lista kentät_nimet sisältää ja jos löydetään pelaajan syöttämä icao koodi
        # päivitetään pelaaja sijainti annettuun icao koodiin
        if loop == 1 or 2:
            for i in kentät_nimet :
                if valittu_kenttä in i :

                    pelaajan_uusi_sijainti = i
                    loop = 3
                    print(f"Pelaajan uusi sijainti {pelaajan_uusi_sijainti[0]} {pelaajan_uusi_sijainti[1]}")
                    break

                # Jos pelaajan antamaa ICAO koodia ei löydy monikosta i muutetaan loop muuttujan arvo 2 jotta ylempänä oleva
                # virhe ilmoitus tulostuu.
                elif valittu_kenttä not in i :
                    loop = 2

        continue
    response = {
        "Name" : pelaajan_uusi_sijainti[0],
        "Icao" : pelaajan_uusi_sijainti[1]
    }
    json_response = json.dumps(response)
    response = Response(response=json_response, status=202, mimetype="application/json")
    response.headers["Content-Type"] = "charset=utf-8"
    return response


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
