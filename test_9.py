#zadanie 9
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import pytest

with open("drugbank_partial.xml", 'r') as file:
    xml_page = file.read()

soup = BeautifulSoup(xml_page, 'xml')
data = soup.find_all(lambda lek: lek.name == 'drug' and lek.has_attr('xmlns'))
wynik = pd.DataFrame({'Stan' : [], 'Ile' : []})

zatw_niewycof = 0

approved = []
withdrawn = []

for lek in data:
    id = lek.find(lambda atr: atr.name == 'drugbank-id' and atr.has_attr('primary')).text
    grupy_grup = lek.findAll('groups')
    for grupa_grup in grupy_grup:
        lista_grup = lek.findAll('group')
        for grupa in lista_grup:
            stan = grupa.text
            if(stan == 'approved'):
                approved.append(id)
            if(stan == 'withdrawn'):
                withdrawn.append(id)
            if(stan == 'experimental' or stan == 'investigational'):
                stan = 'experimental/investigational'
            if(stan in wynik['Stan'].values):
                wynik.loc[wynik['Stan'] == stan, 'Ile'] +=1
            else:
                wynik.loc[len(wynik)] = [stan, 1]

    #wiersze.append(lek_info)

for i in approved:
    if i not in withdrawn:
        zatw_niewycof += 1

def wypisz(val):
    wszystkie = wynik['Ile'].sum()
    return str(round(val / 100 * wszystkie))
print("Liczba zatwierdzonych niewycofanych leków: " + str(zatw_niewycof))

wykres = wynik.set_index('Stan')['Ile'].plot(kind='pie', ylabel = '', autopct = wypisz)

plt.title("Liczba leków danego stanu")
#plt.show()

wynik9 = str(zatw_niewycof)
wynik9_b = wynik

@pytest.mark.parametrize("stan, ile", [('approved', 98),
                                       ('withdrawn', 10),
                                       ('experimental/investigational', 57),
                                       ('vet_approved', 4)])
def test_9(stan, ile):
    wiersz = wynik9_b[wynik9_b["Stan"] == stan]
    assert wiersz['Ile'].values[0] == ile