#zadanie 10 wersja 2
from bs4 import BeautifulSoup
import pandas as pd
import pytest

with open("drugbank_partial.xml", 'r') as file:
    xml_page = file.read()

soup = BeautifulSoup(xml_page, 'xml')
data = soup.find_all(lambda lek: lek.name == 'drug' and lek.has_attr('xmlns'))

wiersze = []
for lek in data:

    id = lek.find(lambda atr: atr.name == 'drugbank-id' and atr.has_attr('primary')).text
    grupy_interakcji = lek.find_all('drug-interactions')
    
    for grupa_interakcji in grupy_interakcji:
        lista_interakcji = grupa_interakcji.find_all('drug-interaction')
        
        for interakcja in lista_interakcji:

            interakcja_info = {
                "ID_leku" : id,
                "Nazwa_leku " : lek.find('name').text,
                "ID leku w interakcji" : interakcja.find('drugbank-id').text,
                "Nazwa leku w interakcji" : interakcja.find('name').text,
                "Opis": interakcja.find('description').text,
            }

            wiersze.append(interakcja_info)
wynik = pd.DataFrame(wiersze)
wynik10 = wynik
wynik


@pytest.mark.parametrize("id, nazwa, id_inter, nazwa_inter", [('DB00001', 'Lepirudin', 'DB06605', 'Apixaban')])
def test_10(id, nazwa, id_inter, nazwa_inter):
    wiersz = wynik10[wynik10["ID_leku"] == id]
    assert wiersz['Nazwa_leku '].values[0] == nazwa
    assert wiersz['ID leku w interakcji'].values[0] == id_inter
    assert wiersz['Nazwa leku w interakcji'].values[0] == nazwa_inter