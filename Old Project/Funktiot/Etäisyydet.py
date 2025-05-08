import mariadb
from geopy import distance


tk_yhteys = mariadb.connect(
    host='localhost',
    port=3306,
    database='peli_projekti',
    user='player',
    password='12345',
    autocommit=True
)

def koordinaatit (pelaajan_vanha_sijainti, pelaajan_sijainti):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{pelaajan_vanha_sijainti[1]}'"
    curs = tk_yhteys.cursor()
    curs.execute(sql)
    tulos = curs.fetchall()
    #valittu_kenttä = input("\nAnna kentän ICAO-koodi jolle haluat lentää = ").upper()
    sql2 = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{pelaajan_sijainti[1]}'"
    curs.execute(sql2)
    tulos2 = curs.fetchall()
    k_etäisyys = round(distance.distance(tulos, tulos2 ).km)
    matka = 0
    u_matka = matka + k_etäisyys

    return k_etäisyys, u_matka, tulos


# pelaajan_sijainti = ["OK", "ESSA"]
#
#
# icao1 = "EFHK"
#
# print(koordinaatit(pelaajan_sijainti, icao1))