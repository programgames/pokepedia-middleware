import csv
import re

import requests
from bs4 import BeautifulSoup

# URL de la page Serebii pour les Pokémon Legends Arceus
url = 'https://www.serebii.net/legendsarceus/hisuipokedex.shtml'

# Récupération de la page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Liste pour stocker les noms des Pokémon
pokemon_names = []

content = soup.find(id="content")

# Sélectionner l'élément 'main' à l'intérieur de l'élément "content"
main = content.find('main')

# Récupérer la 2e table dans l'élément 'main'
table = main.find_all('table')[1]  # Le 2e table a l'index 1

# Parcourir les lignes de la table pour récupérer les noms
for row in table.find_all('tr',recursive=False)[1:]:
    columns = row.find_all('td')
    if columns:
        pokemon_name = columns[3].text.strip()
        pokemon_name = re.sub(r'[^a-zA-Z\s\-]', '', pokemon_name)
        # Le nom est dans la 4e colonne
        pokemon_names.append(pokemon_name.lower())

with open('list.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for pokemon_name in pokemon_names:
        spamwriter.writerow([pokemon_name])
