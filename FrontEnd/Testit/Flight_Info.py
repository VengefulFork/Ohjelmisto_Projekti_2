import mariadb
from geopy import distance
from PythonMain import p
db_connection = mariadb.connect(
    host='localhost',
    port=3306,
    database='peli_projekti',
    user='player',
    password='12345',
    autocommit=True
)

def field_distance (icao) :
    curs = db_connection.cursor()
    sql1 = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{p.current_pos}'"
    curs.execute(sql1)
    old_field = curs.fetchall()
    sql2 = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{icao}'"
    curs.execute(sql2)
    new_field = curs.fetchall()

    t_distance = round(distance.distance(old_field, new_field ).km)

    return t_distance
