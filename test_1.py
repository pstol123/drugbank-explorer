import pytest

# zadanie 1.
import pytest
from bs4 import BeautifulSoup
import pandas as pd
with open("drugbank_partial.xml", 'r') as file:
    xml_page = file.read()

soup = BeautifulSoup(xml_page, 'xml')
data = soup.find_all(lambda lek: lek.name == 'drug' and lek.has_attr('xmlns'))
wiersze = []

for lek in data:
    interakcje = []
    bloki = lek.find_all('food-interactions')
    
    for i in bloki:
        interakcje += i.find_all('food-interaction')
        
    lek_info = {
        'ID' : lek.find(lambda atr: atr.name == 'drugbank-id' and atr.has_attr('primary')).text,
        'Name' : lek.find('name').text,
        'Typ' : lek['type'],
        'Opis' : lek.find('description').text,
        'Postać' : lek.find('state').text,
        'Wskazania' : lek.find('indication').text,
        'Mechanizm działania': lek.find('mechanism-of-action').text,
        'Interakcje z pokarmami': [i.text for i in interakcje]    
    }
    wiersze.append(lek_info)

wynik1 = pd.DataFrame(wiersze)

wynik1

@pytest.mark.parametrize("id, name, typ, postac", [('DB00001', 'Lepirudin', "biotech", 'solid'), ('DB00004', 'Denileukin diftitox', "biotech", 'liquid'), ('DB00106', 'Abarelix', 'small molecule', "solid")])
def test_1(id, name, typ, postac):
    wiersz = wynik1[wynik1["ID"] == id]
    assert wiersz['Name'].values[0] == name
    assert wiersz['Typ'].values[0] == typ
    assert wiersz['Postać'].values[0] == postac
    