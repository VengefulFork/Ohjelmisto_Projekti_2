import mariadb

# from Etäisyydet import koordinaatit


tk_yhteys = mariadb.connect(
        host='localhost',
        port= 3306,
        database= 'peli_projekti',
        user= 'player',
        password= '12345',
        autocommit=True
)

def lentäminen(pelaajan_sijainti):
    # SQL Komentoja varten
    curs = tk_yhteys.cursor()


    # Haetaan kaikki lentoyhtydet joita kentällä jolla pelaaja tällä hetkellä on.
    sql = f"SELECT lopetuspiste FROM airport, yhteys WHERE airport.ident = yhteys.aloituspiste AND ident = '{pelaajan_sijainti[1]}'"
    sql2 = f"SELECT aloituspiste FROM airport, yhteys WHERE airport.ident = yhteys.lopetuspiste AND ident = '{pelaajan_sijainti[1]}'"
    curs.execute(sql)
    yhteydet = curs.fetchall()
    curs.execute(sql2)
    yhteydet.extend(curs.fetchall())

    # Haetaan vielä identia vastaavan kentän nimi pelaajalle
    kentät_nimet = []
    for a in yhteydet :
        curs.execute(f"SELECT name, ident FROM airport WHERE ident = '{a[0]}'")
        kentät_nimet.extend(curs.fetchall())

    # Tulostetaan yhteydet pelaajalle
    print(f"\nOlet kentällä {pelaajan_sijainti[0]}, {pelaajan_sijainti[1]} josta valittavat yhteydet ovat : ")
    for rivi in kentät_nimet :
        print (f"\nKentän nimi on {rivi[0]} ja ICAO-koodi: {rivi[1]}")


    loop = 1

    while loop != 3 :
        # Jos pelaajan antama ICAO koodi on virheellinen tulostetaan uudestaan sijainti ja sieltä olevat kenttä yhteydet
        if loop == 2 :
            print("\nAnnoit Väärän ICAO koodin kokeile uudestaan")
            print(f"\nOlet kentällä {pelaajan_sijainti[0]}, {pelaajan_sijainti[1]} josta valittavat yhteydet ovat : ")
            for rivi in kentät_nimet:
                print(f"\nKentän nimi on {rivi[0]} ja ICAO-koodi: {rivi[1]}")
        #Pyydetään käyttäjältä kenttä jolle haluaa lentää ja poistetaan siitä vielä mahdolliset välilyönnit
        valittu_kenttä = input("\nAnna kentän ICAO-koodi jolle haluat lentää = ").upper().replace(" ", "")
        # Käydään läpi kaikki monikot jota lista kentät_nimet sisältää ja jos löydetään pelaajan syöttämä icao koodi
        # päivitetään pelaaja sijainti annettuun icao koodiin
        if loop == 1 or 2:
            for i in kentät_nimet :
                if valittu_kenttä in i :

                    pelaajan_uusi_sijainti = i
                    loop = 3
                    # print(f"Pelaajan uusi sijainti {pelaajan_uusi_sijainti[0]} {pelaajan_uusi_sijainti[1]}")
                    break

                # Jos pelaajan antamaa ICAO koodia ei löydy monikosta i muutetaan loop muuttujan arvo 2 jotta ylempänä oleva
                # virhe ilmoitus tulostuu.
                elif valittu_kenttä not in i :
                    loop = 2

        continue






    return pelaajan_uusi_sijainti

# pelaajan_sijainti = "ESSA"
#
# lentäminen(pelaajan_sijainti)