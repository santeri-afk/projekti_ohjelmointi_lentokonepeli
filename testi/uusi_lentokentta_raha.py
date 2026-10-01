import random

def anna_rahaa_uudesta_kentasta(kohde, kaydyt_kentat, raha):
    if kohde not in kaydyt_kentat:
        saatu_raha = random.randint(50, 100)
        raha += saatu_raha
        kaydyt_kentat.add(kohde)

        print("Uusi lentokenttä!")
        print("Sait rahaa:", saatu_raha, "€")

    else:
        print("Olet jo käynyt tällä lentokentällä.")
        print("Et saanut rahaa.")

    return raha  