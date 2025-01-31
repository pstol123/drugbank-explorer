#zadanie 7, 8
from bs4 import BeautifulSoup
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pytest

with open("drugbank_partial.xml", 'r') as file:
    xml_page = file.read()

soup = BeautifulSoup(xml_page, 'xml')
data = soup.find_all(lambda lek: lek.name == 'drug' and lek.has_attr('xmlns'))

def wypelnij(pom):
     if(pom is None):
         return "Nieokreślono"
     else:
          if (pom.text == ''):
               return "Nieokreślono"
          return pom.text

wiersze = []

for lek in data:
     grupy_targetow = lek.find_all('targets')

     for grupa_targetow in grupy_targetow:
          targety = grupa_targetow.find_all('target')

          for target in targety:
               poli = target.find("polypeptide")

               if(poli is None):
                    baza = None
                    id_baza = None
               else:
                    baza = poli.get('source')
                    id_baza = poli.get('id')

               grupy_external = target.findAll('external-identifiers')
               gen_id = None

               for grupa_external in grupy_external:
                    lista_external = grupa_external.findAll('external-identifier')
                    for external in lista_external:
                         if(external.find('resource').text == 'GenAtlas'):
                              gen_id = external.find('identifier').text
                
               target_info = {
                    "ID" : wypelnij(target.find("id")),
                    "Zewnętrzna baza" : baza,
                    "ID w bazie" : id_baza,
                    "Nazwa polipeptydu" : wypelnij(target.find("name")),
                    "Nazwa genu kodującego" : wypelnij(target.find("gene-name")),
                    "GenAtlas ID" : gen_id,
                    "Numer chromosomu" : wypelnij(target.find("chromosome-location")),
                    "Lokalizacja w komórce" : wypelnij(target.find("cellular-location"))
               }
               wiersze.append(target_info)

wynik = pd.DataFrame(wiersze)

policzenie = wynik['Lokalizacja w komórce'].value_counts()
wykres = policzenie.plot(kind='pie', autopct='%1.1f%%', labels=None, fontsize=7, figsize=(10,10), pctdistance=1.05, ylabel = '')

plt.legend(labels = policzenie.index, fontsize = 14, loc='center left', bbox_to_anchor=(0.97, 0.5), title = 'Miejsce występowania')
plt.title("Procentowe występowanie targetów w danych częściach komórek", fontsize = 16, y = 0.95, x = 0.9)

#plt.show()

wynik7 = wynik
wynik


@pytest.mark.parametrize("id, id_baza, genatlas, lok", [('BE0000048', 'P00734', 'F2', 'Secreted'),
                                       ('BE0000844', 'P30559', 'OXTR', 'Cell membrane'),
                                       ('BE0000710', 'P12314', 'FCGR1A', 'Cell membrane')])
def test_7(id, id_baza, genatlas, lok):
    wiersz = wynik7[wynik7["ID"] == id]
    assert wiersz['ID w bazie'].values[0] == id_baza
    assert wiersz['GenAtlas ID'].values[0] == genatlas
    assert wiersz['Lokalizacja w komórce'].values[0] == lok
    