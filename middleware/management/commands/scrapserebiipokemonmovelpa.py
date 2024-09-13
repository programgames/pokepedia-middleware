import csv
import os
import tempfile

from django.core.management.base import BaseCommand
from middleware.handler.pokemonmove import pokemonmovehandler
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

from scripts.list_hisui_pokemons import pokemon_names


class Command(BaseCommand):
    help = 'Scrap serebii pokemon mooves'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        # start = kwargs['start']
        # gen = kwargs.get('gen')
        # debug = kwargs.get('debug', False)
        scrap()

def scrape_pokemon_moves(pokemon_url,pokemon_name):
    response = get_item_from_cache(pokemon_name,func= lambda: requests.get(pokemon_url))
    soup = BeautifulSoup(response, 'html.parser')
    moves_by_level = []

    def contains_level_up(h3_tag):
        return 'Standard Level Up' in h3_tag.get_text()

    def contains_others_level_up(h3_tag):
        return ' - Level Up' in h3_tag.get_text()

    lpa = soup.find('div', id='legends')
    h3_tags = lpa.find_all('h3')
    matching_tags = [tag for tag in h3_tags if contains_level_up(tag)]

    for a_tag in matching_tags:
        table = a_tag.find_parent('table')
        if table:
            for row in table.find_all('tr', recursive=False)[1:]:
                columns = row.find_all('td')
                if len(columns) >= 3:
                    if 'Level' == columns[0].text.strip():
                        continue

                    numbers = columns[0].stripped_strings  # récupère tout le texte à l'intérieur du tag

                    # Convertir l'itérateur en une liste pour faciliter l'accès aux éléments
                    numbers_list = list(numbers)

                    # Les nombres "6" et "15" sont respectivement aux positions 1 et 3 dans le texte (ignorer les balises <img>)
                    standard_value = numbers_list[0]
                    mastery_value = numbers_list[1]
                    move = columns[1].text.strip()
                    type_move = columns[2].text.strip()
                    moves_by_level.append({
                        'Level': standard_value,
                        'Mastery': mastery_value,
                        'Move': move,
                        'Type': type_move
                })

    return moves_by_level


def scrape_pokemon_forms(base_url, pokemon_name):
    forms_data = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    forms_data = scrape_pokemon_moves(base_url,pokemon_name)
    time.sleep(1)
    return forms_data

def scrape_all_pokemon(base_url, pokemon_list):
    all_pokemon_data = []

    for pokemon in pokemon_list:
        print(f'Scraping {pokemon}...')
        pokemon_url = f'{base_url}{pokemon}/'
        moves_data = scrape_pokemon_forms(pokemon_url, pokemon)
        all_pokemon_data.append({
            'Pokemon': pokemon,
            'Forms': moves_data
        })
        time.sleep(2)

    return all_pokemon_data

def get_item_from_cache(filename: str, func):
    if os.path.exists('run/cache/' + filename):
        with open('run/cache/' + filename, 'r', encoding='utf-8') as file:
            cached_string = file.read()
            return cached_string

    result = func()
    with open('run/cache/' + filename, 'w+', encoding='utf-8') as file:
        file.write(result.text)
    return result.text

def scrap():
    base_url = 'https://www.serebii.net/pokedex-swsh/'  # URL de base pour les Pokémon sur Serebii
    pokemon_list = []
    with open('scripts/files/hisui.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            pokemon_list.append(row[0])
    pokemon_data = scrape_all_pokemon(base_url, pokemon_list)
    df = pd.DataFrame(pokemon_data)
    df.to_csv('pokemon_moves.csv', index=False)