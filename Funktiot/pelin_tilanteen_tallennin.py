import mariadb

tk_yhteys = mariadb.connect(
    host='localhost',
    port=3306,
    database='peli_projekti',
    user='player',
    password='12345',
    autocommit=True
)

def np_tallenin () :
    c = tk_yhteys.curs
    tallenus = (f"INSERT INTO tallennetut_pelit(pelaajan_nimi, aloitus_kentta, maali, sijainti_kentta, "
                f"pelaajan_kone, kuljettu_matka_km, matkan_aika_min, tuotettu_co2_kg)"
                f"VALUES ()")
    return