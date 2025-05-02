import json

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
def np_tallenin (aloitus_pelaajan_nimi, ensimmäinen_kenttä, maali, pelaajan_sijainti, pelaajan_kone, kokonaan_kuljettu_matka, kokonais_aika, kokonais_co2) :
    c = tk_yhteys.cursor()
    tallenus = (f"INSERT INTO tallennetut_pelit(pelaajan_nimi, aloitus_kentta, maali, sijainti_kentta, "
                f"pelaajan_kone, kuljettu_matka_km, matkan_aika_min, tuotettu_co2_kg)"
                f"VALUES ('{aloitus_pelaajan_nimi[1]}', '{ensimmäinen_kenttä[0]}', '{maali[0][0]}', '{pelaajan_sijainti[0]}',"
                f" '{pelaajan_kone['malli']}', '{kokonaan_kuljettu_matka}', '{kokonais_aika}', '{kokonais_co2}')")
    c.execute(tallenus)
    tk_yhteys.commit()
    return
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/lataus/<nimi>')




def lataus (nimi) :
    print(nimi)
    c = tk_yhteys.cursor()
    tk_lataus = f"SELECT * FROM tallennetut_pelit WHERE pelaajan_nimi = '{nimi}'"
    c.execute(tk_lataus)
    info = c.fetchall()
    vastaus = {
        "Nimi" : info[0][1],
        "Ensimmäinen Kenttä" : info[0][2],
        "Maali" : info[0][3],
        "Sijainti" : info[0][4],
        "Kone" : info[0][5],
        "KM" : info[0][6],
        "Aika" : info[0][7],
        "Co2" : info[0][8],


    }
    json_response = json.dumps(vastaus)
    response = Response(response=json_response, status=202, mimetype="application/json")
    response.headers["Content-Type"] = "charset=utf-8"
    return response

# "TallennusTesti"

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
