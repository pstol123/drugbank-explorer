#zadanie 3 wersja 2.
from bs4 import BeautifulSoup
import pandas as pd
import pytest

with open("drugbank_partial.xml", 'r') as file:
    xml_page = file.read()

soup = BeautifulSoup(xml_page, 'xml')
data = soup.find_all(lambda lek: lek.name == 'drug' and lek.has_attr('xmlns'))

def znajdz_produkty():
    lek = None
    wiersze = []
    for lek_przeg in data:
        id_przeg = lek_przeg.find(lambda atr: atr.name == 'drugbank-id' and atr.has_attr('primary')).text
        lek = lek_przeg
            
        produkty = lek.find_all('products')
        
        for lista_prod in produkty:
            produkty2 = lista_prod.find_all('product')
            
            for produkt in produkty2:
                produkt_info = {
                    "ID_leku" : id_przeg,
                    "Nazwa_produktu " : produkt.find('name').text,
                    "Producent" : produkt.find('labeller').text,
                    "Kod" : produkt.find('ndc-product-code').text,
                    "Postać": produkt.find('dosage-form').text,
                    "Sposób aplikacji" : produkt.find('route').text,
                    "Dawka" : produkt.find('strength').text,
                    "Kraj" : produkt.find('country').text,
                    "Agencja rejestrujące" : produkt.find('source').text
                }

                wiersze.append(produkt_info)
    return pd.DataFrame(wiersze)

wynik3 = znajdz_produkty()
@pytest.mark.parametrize("id, name, kraj", [('DB00001', 'Refludan', 'US'), ('DB00108', 'Tysabri', 'US'), ('DB00104', 'BYNFEZIA Pen', 'US')])

def test_2(id, name, kraj):
    wiersz = wynik3[wynik3["ID_leku"] == id]
    assert wiersz['Nazwa_produktu '].values[0] == name
    assert wiersz['Kraj'].values[0] == kraj