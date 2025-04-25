import mariadb
from flask import Flask

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

def lataus (pelaajan_nimi) :
    c = tk_yhteys.cursor()
    lataus = f"SELECT * FROM tallennetut_pelit WHERE pelaajan_nimi = '{pelaajan_nimi}'"
    c.execute(lataus)
    info = c.fetchall()
    for i in info :
        print(i)
    return

pelaajan_nimi = "TallennusTesti"

lataus (pelaajan_nimi)