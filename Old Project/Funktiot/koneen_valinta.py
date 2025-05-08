from lentokoneet import lentokonetyypit

def koneen_valitsin (lentokonetyypit) :
    print(f"Koneet joilla voit lentää : ")
    b = 0
    for a in lentokonetyypit :
        b += 1
        print(f"{b}. {a['malli']} jonka matkanopeus on {a['max_nopeus_kmh']} km/h ja tuottaa noin {a['hiilidioksidi_per_km']}kg hiilidioksidia per km")
    loop = True
    while loop :
        komento = input("Valitse haluamasi kone syöttämällä joko 1 tai 2 = ").replace(" ", "")
        if komento == "1" :
            pelaajan_kone = lentokonetyypit[0]
            loop = False
        elif komento == "2" :
            pelaajan_kone = lentokonetyypit[1]
            loop = False
        else :
            print("Virheellinen komento kokeile uudestaan")

    return pelaajan_kone



