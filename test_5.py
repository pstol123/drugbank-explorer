#zadanie 5
from bs4 import BeautifulSoup
import pandas as pd
import networkx as nx
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

                for leki in szlak.find_all('drugs'):
                    for lek in leki.find_all('drug'):
                        nazwy_lekow.append(lek.find('name').text)
                        id_lekow.append(lek.find('drugbank-id').text)
                
                szlak_info = {
                    "smpdb-id" : szlak.find("smpdb-id").text,
                    "Nazwa" : szlak.find("name").text,
                    "Nazwy_leków" :  nazwy_lekow,
                    "ID leków" : id_lekow,
                }
                wiersze.append(szlak_info)
    wynik = pd.DataFrame(wiersze)
    return wynik

wyn = znajdz_szlaki()

graph = nx.Graph()
grupaL = []
grupaP = set()
krawedzie = []

for wiersz in wyn.itertuples():
    lek = getattr(wiersz, 'Nazwa')
    pom = getattr(wiersz, 'Nazwy_leków')
    
    for i in range(len(lek)):
        if(lek[i] == ' '):
            lek = lek[:i] + "\n" + lek[(i+1):]
    
    grupaP.update(pom)
    grupaL.append(lek)
    for i in pom:
        krawedzie.append((lek, i))


#plt.figure(figsize=(18,12))
graph.add_nodes_from(grupaL, bipartite=0)
graph.add_nodes_from(grupaP, bipartite=1)
graph.add_edges_from(krawedzie)

pozycje = nx.bipartite_layout(graph, nodes=grupaL)
pozycje.update(nx.bipartite_layout(graph, nodes=grupaP))
for pozycja, (x, y) in pozycje.items():
    pozycje[pozycja] = (y, x)

nx.draw_networkx_nodes(graph, pozycje, node_size=4000)
nx.draw_networkx_edges(graph, pozycje)
nx.draw_networkx_labels(graph, pozycje, font_size=8)

#plt.title("Interakcje leków ze szlakam sygnałowymi")
#plt.show()
wynik5=wyn
wyn

@pytest.mark.parametrize("id, nazwa", [('SMP0000474', 'Cetuximab Action Pathway'),
                                       ('SMP0000265', 'Abciximab Action Pathway'),
                                       ('SMP0000476', 'Trastuzumab Action Pathway')])
def test_5(id, nazwa):
    wiersz = wynik5[wynik5["smpdb-id"] == id]
    assert wiersz['Nazwa'].values == nazwa