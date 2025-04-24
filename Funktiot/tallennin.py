import mariadb

tk_yhteys = mariadb.connect(
    host='localhost',
    port=3306,
    database='peli_projekti',
    user='player',
    password='12345',
    autocommit=True
)

def tk_tallenin (aloitus_pelaajan_nimi, ensimmäinen_kenttä, maali, kokonaan_kuljettu_matka, kokonais_aika, kokonais_co2, pisteet):
    curs = tk_yhteys.cursor()
    # Onnistuneesti suoritetun pelin jälkeen tallenetaan tietokantaa seuraavat tiedot
    tallenus = (f"INSERT INTO edelliset_pelit (pelaajan_nimi, aloitus_kentta, maali, kuljettu_matka_km, matkan_aika_min, tuotettu_co2_kg, pisteet)"
                f"VALUES ('{aloitus_pelaajan_nimi[1]}', '{ensimmäinen_kenttä[0]}', '{maali[0][0]}', '{kokonaan_kuljettu_matka}', '{kokonais_aika}', '{kokonais_co2}', '{pisteet}') ")
    curs.execute(tallenus)
    tk_yhteys.commit()

    return

def edelliset_pelit ():
    loop = True
    while loop :
        komento = input("\nSyötä 1 jos haluat katsoa edelliset pelit tai 2 aloittaaksesi uuden pelin = ").replace(" ", "")
        # Haetaan kaikki pelit jotka on onnistuneesti pelattu loppuun saakka
        if komento == "1" :
            curs = tk_yhteys.cursor()
            sql = (f"SELECT ID, pelaajan_nimi, pisteet FROM edelliset_pelit")
            curs.execute(sql)
            edelliset_pelaajat = curs.fetchall()
            # Tulostetaan pelaajalle niistä infoa
            for a in edelliset_pelaajat :
                print(f"Peli {a[0]}, pelaajan nimi {a[1]}, pisteet {a[2]}")


        elif komento == "2" :
            print("Uusi peli alkaa")
            loop = False
        else :
            print("Virheellinen komento syötä uudestaan")
    return


