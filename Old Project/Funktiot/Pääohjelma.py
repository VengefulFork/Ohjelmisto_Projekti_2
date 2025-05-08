from Reitinluoja import reitinluoja
from Lentäminen import lentäminen
from lentokoneet import lentokonetyypit
from koneen_valinta import koneen_valitsin
from Etäisyydet import koordinaatit
from Matkanlaskija import lennon_tiedot_laskin
from komennot import komennot
from kartta import kartta
from tarina import tarina, info
from clear import clear
from tallennin import tk_tallenin, edelliset_pelit
from Pisteytys import piste_laskuri
from pelin_tilanteen_tallennin import np_tallenin

def pääohjelma () :
    # Pääohjelmassa tarvittavia muuttujia
    koko_reitti = reitinluoja()
    maali = koko_reitti[1]
    pelaajan_sijainti = koko_reitti[0]
    ensimmäinen_kenttä = pelaajan_sijainti
    intro = (f"Aloitat kentältä {pelaajan_sijainti[0]},{pelaajan_sijainti[1]} onnea matkaan Agentti!")
    kokonaan_kuljettu_matka = 0
    kokonais_aika = 0
    kokonais_co2 = 0



    edelliset_pelit()

    aloitus_pelaajan_nimi = tarina(maali)

    if aloitus_pelaajan_nimi[0] == "1" :

        print(intro)
        while maali[0][1] != pelaajan_sijainti[1] :

                komennot()
                komento = input("Anna haluamasi komennon numero = ").replace(" ", "")
                if komento == "1" :
                    kartta()
                # Pelaajan siirtämiseen tarvittavien funktioiden kutsuminen
                elif komento == "2" :
                    pelaajan_vanha_sijainti = pelaajan_sijainti
                    pelaajan_sijainti = lentäminen(pelaajan_sijainti)

                    pelaajan_kone = koneen_valitsin(lentokonetyypit)

                    matka = koordinaatit(pelaajan_vanha_sijainti, pelaajan_sijainti)[0]
                    lennon_tiedot = lennon_tiedot_laskin(matka, pelaajan_kone)

                    print(f"\nMatkasi kentältä {pelaajan_vanha_sijainti[0]} kentälle {pelaajan_sijainti[0]}\n"
                          f"oli {matka} kilometria ja valitsemallasi koneella {pelaajan_kone['malli']} siihen meni {lennon_tiedot[0]}"
                          f" minuuttia josta {lennon_tiedot[2]} minuuttia meni kentällä ja tuotti {lennon_tiedot[1]} kiloa hiilidioksidia")
                    # Lisätään matkan data muuttujiin myöhempää käyttöä varten
                    kokonaan_kuljettu_matka += matka
                    kokonais_aika += lennon_tiedot[0]
                    kokonais_co2  += lennon_tiedot[1]
                elif komento == "3" :
                    print(f"Maalisi on {maali[0][0]}, {maali[0][1]}")
                elif komento == "4" :
                    print(f"Olet matkustanut {kokonais_aika} minuuttia, {kokonaan_kuljettu_matka} km ja olet tuottanut {kokonais_co2} kg hiilidioksidia")
                elif komento == "5" :
                    info()
                elif komento == "6" :
                    clear()
                elif komento == "7" :
                    np_tallenin(aloitus_pelaajan_nimi, ensimmäinen_kenttä, maali, pelaajan_sijainti, pelaajan_kone, kokonaan_kuljettu_matka, kokonais_aika, kokonais_co2)
                else :
                    print("Virheellinen komento kokeile uudestaan")
        pisteet = piste_laskuri(kokonaan_kuljettu_matka, kokonais_aika, kokonais_co2)
        print(f"\nSaavuit kohteeseesi {maali[0][0]} ja Tohtori Palmu on jälleen vangittu. Onnittelumme Agentti {aloitus_pelaajan_nimi[1]}.")
        print(f"\nMatkasi kesti {kokonais_aika} minuuttia, ja sen pituus oli {kokonaan_kuljettu_matka} km ja olet tuottanut {kokonais_co2} kg hiilidioksidia. Sait {pisteet} pistettä.")
        # Kutsutaan tietokantaan tallentamiseen tarkoitettu funktio
        tk_tallenin(aloitus_pelaajan_nimi, ensimmäinen_kenttä, maali, kokonaan_kuljettu_matka, kokonais_aika, kokonais_co2, pisteet)
    elif aloitus_pelaajan_nimi[1] == "2" :
        print("Olemme pettyneitä :(")
    return

pääohjelma()


