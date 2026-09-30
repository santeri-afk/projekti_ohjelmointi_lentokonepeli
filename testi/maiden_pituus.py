
from geopy.distance import geodesic

def maiden_pituus(maa1, maa2):
    tulos1 = (hae_kentta_tiedot(yhteys, maa1)["latitude_deg"], hae_kentta_tiedot(yhteys, maa1)["longitude_deg"])

    tulos2 = (hae_kentta_tiedot(yhteys, maa2)["latitude_deg"], hae_kentta_tiedot(yhteys, maa2)["longitude_deg"])
    return (geodesic(tulos1, tulos2).km)

print(maiden_pituus("EFHK", "EDDF"))
