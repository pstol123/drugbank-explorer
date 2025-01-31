#zadanie 2
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
    synonimy = []
    pom = lek.find_all('synonyms')
    
    for i in pom:
        synonimy += i.find_all('synonym')
    
    lek_info = {
        'ID' : lek.find(lambda atr: atr.name == 'drugbank-id' and atr.has_attr('primary')).text,
        'Name' : lek.find('name').text,
        'Synonimy' : [i.text for i in synonimy]    
    }
    
    wiersze.append(lek_info)

wynik2 = pd.DataFrame(wiersze)



def znajdz_synonimy(id):
    if id not in wynik2['ID'].values:
        print("Podano błędne id.")
        return
    
    syno = wynik2.loc[wynik2['ID'] == id, 'Synonimy'].values[0]
    name = wynik2.loc[wynik2['ID'] == id, 'Name'].values[0] 
    
    graph = nx.Graph()
    graph.add_nodes_from(syno)
    
    krawedzie = []
    for i in syno:
        if(i != name):
            krawedzie.append((i, name))
    graph.add_edges_from(krawedzie)
    
    pozycje = nx.kamada_kawai_layout(graph)

    plt.figure(figsize=(16,12))
    
    nx.draw_networkx_edges(graph, pozycje)
    etykiety = {i: str(i) for i in graph.nodes()}
    nx.draw_networkx_nodes(graph, pozycje, alpha=1, node_color="white", node_size=5000)
    nx.draw_networkx_labels(graph, pozycje, labels=etykiety, font_size=8)
    
    plt.xlim(-2, 2)
    plt.title("Synonimy leku " +  str(name))
    #plt.show()

znajdz_synonimy('DB00003')

wynik2

@pytest.mark.parametrize("id, name", [('DB00001', 'Lepirudin'), ('DB00004', 'Denileukin diftitox'), ('DB00106', 'Abarelix')])
def test_2(id, name):
    wiersz = wynik2[wynik2["ID"] == id]
    assert wiersz['Name'].values[0] == name