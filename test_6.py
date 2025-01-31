#zadanie 6
from bs4 import BeautifulSoup
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pytest

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
    }
    wiersze.append(lek_info)

wynik = pd.DataFrame(wiersze)
wynik['Liczba'] = 0

data = soup.find_all(lambda lek: lek.name == 'drug' and lek.has_attr('xmlns'))

wiersze = []
for lek in data:
    grupy_szlakow = lek.find_all('pathways')
    for lista_szlakow in grupy_szlakow:
        szlaki = lista_szlakow.find_all('pathway')
        for szlak in szlaki:
            nazwy_lekow = []
            id_lekow = []

            for leki in szlak.find_all('drugs'):
                for lek in leki.find_all('drug'):
                    id = lek.find('drugbank-id').text
                    pom = wynik.loc[wynik['ID'] == id, 'Liczba']
                    if(pom.empty):
                        continue
                        #gdy chcemu uwzględnić również leki niebędące w 100 opisanych:
                        #wynik.loc[len(wynik)] = [id, 0]
                    wynik.loc[wynik['ID'] == id, 'Liczba'] +=1

wynik['Liczba'].hist()

plt.title('Histogram liczby interakcji leków ze szlakami')
plt.xlabel('Liczba interakcji ze szlakami')
plt.ylabel('Liczba leków')

#plt.show()

wynik6 = wynik
wynik


@pytest.mark.parametrize("id, liczba", [('DB00001', 1), ('DB00004', 0), ('DB00106', 0)])
def test_6(id, liczba):
    wiersz = wynik6[wynik6["ID"] == id]
    assert wiersz['Liczba'].values[0] == liczba