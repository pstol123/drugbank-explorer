import pytest
#zadanie 12
from bs4 import BeautifulSoup
import pandas as pd
import requests

#będę używał bazy UniProt

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
            poli = target.find_all("polypeptide")
            
            for peptyd in poli:
                baza = peptyd.get('source')
                id_baza = peptyd.get('id')

                url  = "https://rest.uniprot.org/uniprotkb/" + id_baza +'.xml'
                odpowiedz = requests.get(url)

                if(odpowiedz.status_code != 200):
                    print('Blad')
                    continue
                soup2 = BeautifulSoup(odpowiedz.text, 'xml')
                protein = soup2.find('protein')
                
                if(protein is None):
                    continue
                
                rec_name = protein.find('recommendedName')
                alt_name = protein.find('alternativeName')
                if(alt_name is None):
                    alt_name_full = 'Nieokreślono'
                else:
                    alt_name_full = wypelnij(alt_name.find('fullName'))
                
                target_info = {
                    "ID leku" : lek.find(lambda atr: atr.name == 'drugbank-id' and atr.has_attr('primary')).text,
                    "Nazwa leku" : wypelnij(lek.find('name')),
                    "ID polipeptydu" : id_baza,
                    "Nazwa": soup2.find('name'),
                    "Białko - nazwa rekomendowana" : wypelnij(rec_name.find('fullName')),
                    "Białko - nazwa alternatywna" : alt_name_full,
                    "Organizmy" : soup2.find('organism').find('name'),
                    "Długość sekwencji" : soup2.find('sequence').get('length'),
                    "Masa cząsteczkowa" : soup2.find('sequence').get('mass'),
                    "Existance" : soup2.find('proteinExistence').get('type')
                
                }
                
                wiersze.append(target_info)


wynik = pd.DataFrame(wiersze)
wynik12 = wynik
wynik


@pytest.mark.parametrize("id, id_peptydu, bialko", [('DB00001', 'P00734', 'Prothrombin'),
                                                              ('DB00002', 'P00533', 'Epidermal growth factor receptor'),
                                                              ('DB00108', 'P13612', 'Integrin alpha-4')])
def test_12(id, id_peptydu, bialko):
    wiersz = wynik12[wynik12["ID leku"] == id]
    assert wiersz['ID polipeptydu'].values[0] == id_peptydu
    assert wiersz['Białko - nazwa rekomendowana'].values[0] == bialko