import json
import random
from geopy import distance
from lentokoneet import lentokonetyypit
import mariadb
from flask import Flask, Response
from flask_cors import CORS
import random


db_connection = mariadb.connect(
    host='localhost',
    port=3306,
    database='peli_projekti',
    user='player',
    password='12345',
    autocommit=True
)
class Player :
    co2 = 0
    distance_km = 0
    time_min = 0
    plane = lentokonetyypit[0]
    start_pos = []
    end_pos = []
    current_pos = ""
    old_pos = ""
    game_status = ""

p = Player
def flight_info (icao) :
    # Calculating distance between player's current position and future position
    curs = db_connection.cursor()
    sql1 = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{p.current_pos}'"
    curs.execute(sql1)
    old_field = curs.fetchall()
    sql2 = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{icao}'"
    curs.execute(sql2)
    new_field = curs.fetchall()
    t_distance = round(distance.distance(old_field, new_field ).km)

    #Time spent on flight in mins
    flight_time = round(t_distance/ p.plane['max_nopeus_kmh']*60)
    #Random extra time to simulate switching to connecting flight
    switch_time = random.randint(15, 30)
    flight_time += switch_time
    #Calculating co2 spent on flight based off of plane characteristics
    #First multiply distance by plane fuel per km
    fuel_consumed = t_distance * p.plane['poltoaineen_kulutus_kg/km']
    #Then multiply by 3.16 for approx co2 produced
    produced_co2 = fuel_consumed * 3.16
    flight_data = {
        "Distance" : t_distance,
        "Time" : flight_time,
        "Co2" : round(produced_co2)
    }
    return flight_data
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/gameStart/<name>')
def game_start(name) :
    def route_maker():
        kentät_icao = ("EFHK", "EFKT", "ESSA", "ENGM", "ENTC", "BIKF", "EGPD", "EGLL", "LFPG", "LEMD",
                       "LIRF", "LSZH", "EDDB", "EPWA", "EKBI", "EVRA", "LOWW", "LRBS", "LQSA", "LGAV", "EHAM")
        # RNG aloitus ja lopetus kenttien arpomista varten.
        aloitus_kenttä = kentät_icao[random.randint(0, 20)]
        lopetus_kenttä = kentät_icao[random.randint(0, 20)]
        # Testataan ovatko aloitus_kenttä ja lopetus_kenttä samat ja jos on niin arvotaan uusi lopetus_kenttä
        if aloitus_kenttä == lopetus_kenttä:
            lopetus_kenttä = kentät_icao[random.randint(0, 20)]
        # sql haut
        sql_aloitus = f"SELECT name, ident FROM airport WHERE ident = '{aloitus_kenttä}'"
        sql_lopetus = f"SELECT name, ident FROM airport WHERE ident = '{lopetus_kenttä}'"

        curs = db_connection.cursor()

        curs.execute(sql_aloitus)
        aloitus_kenttä = curs.fetchall()
        # Käydään läpi sql haun palauttama lista joka sisältää monikon ja määritellään aloitus_kenttä täksi monikoksi
        for i in aloitus_kenttä:
            aloitus_kenttä = i

        curs.execute(sql_lopetus)
        lopetus_kenttä = curs.fetchall()

        testaus = True
        while testaus:
            # Haetaan aloituskentällä olevat yhteydet
            sql_testaus1 = f"SELECT lopetuspiste FROM airport, yhteys WHERE airport.ident = yhteys.aloituspiste AND ident = '{aloitus_kenttä[1]}'"
            sql_testaus2 = f"SELECT aloituspiste FROM airport, yhteys WHERE airport.ident = yhteys.lopetuspiste AND ident = '{aloitus_kenttä[1]}'"
            curs.execute(sql_testaus1)
            testaus_yhteydet = curs.fetchall()
            curs.execute(sql_testaus2)
            testaus_yhteydet.extend(curs.fetchall())

            # Käydään läpi kaikki aloitus kentällä olevat yhteydet
            for i in testaus_yhteydet:
                # Jos aloitus kenttältä on yhteys lopetus kentälle arvotaan uusi aloitus kenttä tai jos ne ovat sama kenttä arvotaan uusi kenttä
                if lopetus_kenttä[0][1] in i or aloitus_kenttä[1] == lopetus_kenttä[0][1]:

                    sql = f"SELECT name, ident FROM airport WHERE ident ='{kentät_icao[random.randint(0, 20)]}'"
                    curs.execute(sql)
                    aloitus_kenttä = curs.fetchall()
                    # Käydään läpi sql haun palauttama lista joka sisältää monikon ja määritellään aloitus_kenttä täksi monikoksi
                    for a in aloitus_kenttä:
                        aloitus_kenttä = a

                    break
                # Jos lopetus kenttä ei ole aloitus kentän yhteyksissä rikotaan silmukka
                if lopetus_kenttä[0][1] not in i:
                    testaus = False
            continue
        fields = []
        fields.append(aloitus_kenttä)
        fields.append(lopetus_kenttä)
        return fields
    start_end = route_maker()
    p.game_status = ""
    p.plane = lentokonetyypit[0]
    p.co2 = 0
    p.time_min = 0
    p.distance_km = 0
    p.name = name
    p.start_pos = start_end[0]
    p.end_pos = start_end[1][0]
    p.current_pos = start_end[0][1]
    print(p.current_pos)
    r = []
    a = {
        "Name": p.start_pos[0],
        "Icao": p.start_pos[1],
    }
    r.append(a)
    b = {
        "Name": p.end_pos[0],
        "Icao": p.end_pos[1],
    }
    r.append(b)
    c = {
        "Icao": p.start_pos[1],
    }
    r.append(c)
    json_response = json.dumps(r)
    response = Response(response=json_response, status=202, mimetype="application/json")
    response.headers["Content-Type"] = "charset=utf-8"
    print("Function was called from JS")
    return response
@app.route('/mapDrawer/')
def map_drawer ():
    c = db_connection.cursor()
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
@app.route('/connections/<icao>')
def connections (icao):
    c = db_connection.cursor()
    sql = f"SELECT lopetuspiste FROM airport, yhteys WHERE airport.ident = yhteys.aloituspiste AND ident = '{icao}'"
    sql2 = f"SELECT aloituspiste FROM airport, yhteys WHERE airport.ident = yhteys.lopetuspiste AND ident = '{icao}'"
    c.execute(sql)
    conn = c.fetchall()
    c.execute(sql2)
    conn.extend(c.fetchall())

    r = []
    for i in conn :
        r.append(i)
    json_response = json.dumps(r)
    response = Response(response=json_response, status=202, mimetype="application/json")
    response.headers["Content-Type"] = "charset=utf-8"
    return response
@app.route('/status/')
def status ():
    b = {
        "Icao" : p.current_pos,
        "IcaoEnd" : p.end_pos[1],
        "Km": p.distance_km,
        "Co2" : p.co2,
        "Time" : p.time_min,
        "Plane" : p.plane,
        "GameStatus" : p.game_status
    }
    # print("Player current position is" + p.current_pos)
    json_response = json.dumps(b)
    response = Response(response=json_response, status=202, mimetype="application/json")
    response.headers["Content-Type"] = "charset=utf-8"
    return response

@app.route('/flying/<icao>')
def flying (icao):
    p.old_pos = p.current_pos
    curs = db_connection.cursor()
    sql = f"SELECT lopetuspiste FROM airport, yhteys WHERE airport.ident = yhteys.aloituspiste AND ident = '{p.current_pos}'"
    sql2 = f"SELECT aloituspiste FROM airport, yhteys WHERE airport.ident = yhteys.lopetuspiste AND ident = '{p.current_pos}'"
    curs.execute(sql)
    conn = curs.fetchall()
    curs.execute(sql2)
    conn.extend(curs.fetchall())

    options = []

    for a in conn :
        # print(a[0])
        curs.execute(f"SELECT ident FROM airport WHERE ident ='{a[0]}'")
        options.extend(curs.fetchall())
    #Storing data from the flight to the p object
    flight_data = flight_info(icao)
    p.distance_km += flight_data['Distance']
    p.time_min += flight_data['Time']
    p.co2 += flight_data['Co2']
    for i in options :
        if icao in i :
            p.current_pos = i[0]
    if p.current_pos == p.end_pos[1] :
        p.game_status = "WON"
    a = {
        "OldPos" : p.old_pos,
        "NewPos" : p.current_pos
    }
    json_response = json.dumps(a)
    response = Response(response=json_response, status=202, mimetype="application/json")
    response.headers["Content-Type"] = "charset=utf-8"
    return response

@app.route('/distance/<icao>')
def distance_calculation (icao):
    data = flight_info(icao)
    b = {
        "Distance" : data['Distance'],
        "Time" : data['Time'],
        "Co2" : data['Co2']
    }
    json_response = json.dumps(b)
    response = Response(response=json_response, status=202, mimetype="application/json")
    response.headers["Content-Type"] = "charset=utf-8"
    return response

@app.route('/plane/')
def plane_switcher():
    if p.plane['malli'] == lentokonetyypit[0]['malli'] :
        p.plane = lentokonetyypit[1]
    elif p.plane['malli'] == lentokonetyypit[1]['malli']:
        p.plane = lentokonetyypit[0]


    b = {
        "New Plane" : p.plane
    }

    json_response = json.dumps(b)
    response = Response(response=json_response, status=202, mimetype="application/json")
    response.headers["Content-Type"] = "charset=utf-8"
    return response


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
