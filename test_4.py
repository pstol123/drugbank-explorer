#zadanie 4
from bs4 import BeautifulSoup
import pandas as pd
import pytest

with open("drugbank_partial.xml", 'r') as file:
    xml_page = file.read()

soup = BeautifulSoup(xml_page, 'xml')
data = soup.find_all(lambda lek: lek.name == 'drug' and lek.has_attr('xmlns'))

def znajdz_szlaki():
    wiersze = []
    for lek in data:
        grupy_szlakow = lek.find_all('pathways')
        for lista_szlakow in grupy_szlakow:
            szlaki = lista_szlakow.find_all('pathway')
            for szlak in szlaki:
                nazwy_lekow = []
                id_lekow = []
                enzymy = []

                for leki in szlak.find_all('drugs'):
                    for lek in leki.find_all('drug'):
                        nazwy_lekow.append(lek.find('name').text)
                        id_lekow.append(lek.find('drugbank-id').text)
                
                for enzym in szlak.find_all('enzymes'):
                    enzymy += enzym.find_all('uniprot-id')

                szlak_info = {
                    "ID_leku" : lek.find("drugbank-id").text,
                    "smpdb-id" : szlak.find("smpdb-id").text,
                    "Nazwa" : szlak.find("name").text,
                    "Kategoria" : szlak.find("category").text,
                    "Nazwy leków" :  nazwy_lekow,
                    "ID leków" : id_lekow,
                    "Enzymy" : enzymy
                }
                wiersze.append(szlak_info)
    wynik = pd.DataFrame(wiersze)
    return wynik, wynik.shape[0]

wyn = znajdz_szlaki()
print(wyn[1])
wynik4 = wyn[0]
wynik4

@pytest.mark.parametrize("id, smpdb, nazwa, kategoria", [('DB00002', 'SMP0000474', 'Cetuximab Action Pathway', 'drug_action'),
                                                             ('DB00054', 'SMP0000265', 'Abciximab Action Pathway', 'drug_action'),
                                                             ('DB00072', 'SMP0000476', 'Trastuzumab Action Pathway', 'drug_action')])
def test_4(id, smpdb, nazwa, kategoria):
    wiersz = wynik4[wynik4["ID_leku"] == id]
    assert wiersz['smpdb-id'].values[0] == smpdb
    assert wiersz['Nazwa'].values[0] == nazwa
    assert wiersz['Kategoria'].values[0] == kategoria
