import csv
import os

from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup


from pokeapi.pokemon_v2.models import Pokemon, Move
class Command(BaseCommand):
    help = 'Scrap serebii pokemon mooves'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        scrap()

def scrape_pokemon_moves(pokemon_url,pokemon_name):
    def do_request(pokemon_url):
        print('request for' + pokemon_url)
        return requests.get(pokemon_url)
    response = get_item_from_cache(pokemon_name,func= lambda: do_request(pokemon_url))
    soup = BeautifulSoup(response, 'html.parser')
    moves_by_level = {}

    def contains_level_up(h3_tag):
        return 'Standard Level Up' in h3_tag.get_text()
    def all_lvl_up(h3_tag):
        return 'Level Up' in h3_tag.get_text()

    def specific_lvl_up(h3_tag):
        return ' - Level Up' in h3_tag.get_text()

    def specific_lvl_up_2(h3_tag):
        return 'Level Up - ' in h3_tag.get_text()

    def hisuiasian_lvl_up(h3_tag):
        return 'Hisuian Form Level Up' in h3_tag.get_text()
    def move_shop(h3_tag):
        return 'Move Shop Attacks' in h3_tag.get_text()

    lpa = soup.find('div', id='legends')
    if not lpa:
        a = soup.find('a', attrs={'name': 'legendsattacks'})
        lpa = a.find_next('table')
    h3_tags = lpa.find_all('h3')
    specific_lvl_up_tags = [tag for tag in h3_tags if specific_lvl_up(tag)]
    specific_lvl_up_tags2 = [tag for tag in h3_tags if specific_lvl_up_2(tag)]
    hisuiasian_lvl_up_tags = [tag for tag in h3_tags if hisuiasian_lvl_up(tag)]
    matching_tags = [tag for tag in h3_tags if contains_level_up(tag)]
    move_shop_tags = [tag for tag in h3_tags if move_shop(tag)]

    if len(move_shop_tags) > 1:
        raise Exception
    moves_by_level['Shop'] =[]


    if len(specific_lvl_up_tags) > 0:
        matching_tags = [tag for tag in h3_tags if all_lvl_up(tag)]
        for a_tag in matching_tags:
            moves_by_level[a_tag] = []
            table = a_tag.find_parent('table')
            if table:
                for row in table.find_all('tr', recursive=False)[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 8 and (a_tag.text != 'Move Shop Attacks' and  pokemon_name not in ['sneasel','wormadam']):
                        print('FORM FOR' + pokemon_name)
                    if len(columns) >= 3:
                        if 'Level' == columns[0].text.strip():
                            continue

                        numbers = columns[0].stripped_strings  # récupère tout le texte à l'intérieur du tag

                        # Convertir l'itérateur en une liste pour faciliter l'accès aux éléments
                        numbers_list = list(numbers)

                        # Les nombres "6" et "15" sont respectivement aux positions 1 et 3 dans le texte (ignorer les balises <img>)
                        standard_value = numbers_list[0]
                        mastery_value = numbers_list[1] if len(numbers_list) > 1 else None
                        move = columns[1].text.strip()
                        type_move = columns[2].text.strip()
                        moves_by_level.append({
                            'Level': standard_value,
                            'Mastery': mastery_value,
                            'Move': move,
                            'Type': type_move
                        })

        for move in move_shop_tags:
            table = move.find_parent('table')
            if table:
                for row in table.find_all('tr', recursive=True)[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 7:
                        print('FORM FOR' + pokemon_name)
                    if len(columns) >= 3:
                        if 'Attack Name' == columns[0].text.strip():
                            continue
                        moveT = columns[0].text.strip()
                        moves_by_level['Shop'].append({
                            'Move': moveT,
                        })
        return moves_by_level

    if len(specific_lvl_up_tags2) > 0:
        matching_tags = [tag for tag in h3_tags if all_lvl_up(tag)]
        for a_tag in matching_tags:
            moves_by_level[a_tag.text] = []
            table = a_tag.find_parent('table')
            if table:
                for row in table.find_all('tr', recursive=False)[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 8 and (a_tag.text != 'Move Shop Attacks' and  pokemon_name not in ['sneasel','wormadam']):
                        print('FORM FOR' + pokemon_name)
                    if len(columns) >= 3:
                        if 'Level' == columns[0].text.strip():
                            continue

                        numbers = columns[0].stripped_strings  # récupère tout le texte à l'intérieur du tag

                        # Convertir l'itérateur en une liste pour faciliter l'accès aux éléments
                        numbers_list = list(numbers)

                        # Les nombres "6" et "15" sont respectivement aux positions 1 et 3 dans le texte (ignorer les balises <img>)
                        standard_value = numbers_list[0]
                        mastery_value = numbers_list[1] if len(numbers_list) > 1 else None
                        move = columns[1].text.strip()
                        type_move = columns[2].text.strip()
                        moves_by_level[a_tag.text].append({
                            'Level': standard_value,
                            'Mastery': mastery_value,
                            'Move': move,
                            'Type': type_move
                        })
        for move in move_shop_tags:
            table = move.find_parent('table')
            if table:
                for row in table.find_all('tr', recursive=True)[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 7:
                        alt_texts = [img['alt'] for img in columns[7].find_all('img')]
                        print('FORM FOR' + pokemon_name)
                    if len(columns) >= 3:
                        if 'Attack Name' == columns[0].text.strip():
                            continue
                        moveT = columns[0].text.strip()
                        if moveT == '':
                            continue
                        moves_by_level['Shop'].append({
                            'Move': moveT,
                            'Form': alt_texts
                        })
        return moves_by_level

    if len(hisuiasian_lvl_up_tags) > 0:
        matching_tags = [tag for tag in h3_tags if all_lvl_up(tag)]
        if len(matching_tags) > 1 and pokemon_name not in ['sneasel']:
            raise Exception('Multiple Hisuian Level Up Tags Found')
        for a_tag in matching_tags:
            form_name = a_tag.get_text(strip=True)
            table = a_tag.find_parent('table')
            moves_by_level[form_name] = []
            if table:
                for row in table.find_all('tr', recursive=False)[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 8 and (form_name != 'Move Shop Attacks' and  pokemon_name not in ['sneasel','wormadam']):
                        print('FORM FOR' + pokemon_name)
                    if len(columns) >= 3:
                        if 'Level' == columns[0].text.strip():
                            continue

                        numbers = columns[0].stripped_strings  # récupère tout le texte à l'intérieur du tag

                        # Convertir l'itérateur en une liste pour faciliter l'accès aux éléments
                        numbers_list = list(numbers)

                        # Les nombres "6" et "15" sont respectivement aux positions 1 et 3 dans le texte (ignorer les balises <img>)
                        standard_value = numbers_list[0]
                        mastery_value = numbers_list[1] if len(numbers_list) > 1 else None
                        move = columns[1].text.strip()
                        type_move = columns[2].text.strip()
                        moves_by_level[form_name].append({
                            'Level': standard_value,
                            'Mastery': mastery_value,
                            'Move': move,
                            'Type': type_move
                    })
        for move in move_shop_tags:
            table = move.find_parent('table')
            if table:
                for row in table.find_all('tr', recursive=True)[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 7:
                        alt_texts = [img['alt'] for img in columns[7].find_all('img')]
                        print('FORM FOR' + pokemon_name)
                    if len(columns) >= 3:
                        if 'Attack Name' == columns[0].text.strip():
                            continue
                        moveT = columns[0].text.strip()
                        moves_by_level['Shop'].append({
                            'Move': moveT,
                            'Form': alt_texts
                        })
        return moves_by_level

    if len(matching_tags) > 0:
        moves_by_level['Standard Level Up'] = []
        for a_tag in matching_tags:
            table = a_tag.find_parent('table')
            if table:
                for row in table.find_all('tr', recursive=False)[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 8 and (a_tag.text != 'Move Shop Attacks' and  pokemon_name not in ['sneasel','wormadam']):
                        print('FORM FOR' + pokemon_name)
                    if len(columns) >= 3:
                        if 'Level' == columns[0].text.strip():
                            continue

                        numbers = columns[0].stripped_strings  # récupère tout le texte à l'intérieur du tag

                        # Convertir l'itérateur en une liste pour faciliter l'accès aux éléments
                        numbers_list = list(numbers)

                        # Les nombres "6" et "15" sont respectivement aux positions 1 et 3 dans le texte (ignorer les balises <img>)
                        standard_value = numbers_list[0]
                        mastery_value = numbers_list[1] if len(numbers_list) > 1 else None
                        move = columns[1].text.strip()
                        type_move = columns[2].text.strip()
                        moves_by_level['Standard Level Up'].append({
                            'Level': standard_value,
                            'Mastery': mastery_value,
                            'Move': move,
                            'Type': type_move
                    })
        for move in move_shop_tags:
            table = move.find_parent('table')
            if table:
                for row in table.find_all('tr', recursive=True)[1:]:
                    columns = row.find_all('td')
                    alt_texts = ''
                    if len(columns) > 7:
                        print('FORM FOR' + pokemon_name)
                        alt_texts = [img['alt'] for img in columns[7].find_all('img')]
                    if len(columns) >= 3:
                        if 'Attack Name' == columns[0].text.strip():
                            continue
                        moveT = columns[0].text.strip()
                        moves_by_level['Shop'].append({
                            'Move': moveT,
                            'Form': alt_texts
                        })
        return moves_by_level


def scrape_pokemon_forms(base_url, pokemon_name):
    forms_data = scrape_pokemon_moves(base_url,pokemon_name)
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
    pokemon_datas = scrape_all_pokemon(base_url, pokemon_list)


    with open('lpa.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['pokemon_id', 'version_group_id', 'move_id','pokemon_move_method_id', 'level','order','mastery'])
        for pokemon_data in pokemon_datas:
            if len(pokemon_data['Forms']) > 2:
                if list(pokemon_data['Forms'].items())[1][0] == 'Hisuian Form Level Up':
                    for formname, data in pokemon_data['Forms'].items():
                        if formname == 'Hisuian Form Level Up':
                            pokemon = Pokemon.objects.get(name=pokemon_data['Pokemon']+'-hisui')
                            for move in pokemon_data['Forms']['Hisuian Form Level Up']:
                                moveE = Move.objects.get(name=move['Move'].lower().replace(' ', '-'))
                                writer.writerow([pokemon.id, 24, moveE.id, 1,move['Level'], None, move['Mastery']])
                        elif formname == 'Standard Level Up':
                            pkmname = pokemon_data['Pokemon'].replace(' ', '-')
                            pokemon = Pokemon.objects.get(name=pkmname)
                            for move in data:
                                moveE = Move.objects.get(name=move['Move'].lower().replace(' ', '-'))
                                writer.writerow([pokemon.id, 24, moveE.id, 1,move['Level'], None, move['Mastery']])
                        elif formname == 'Shop':
                            for move in pokemon_data['Forms']['Shop']:
                                movestr = move['Move'].lower().replace(' ', '-')
                                for form in move['Form']:
                                    if form == 'Wormadam':
                                        form = 'wormadam-plant'
                                    elif form == 'Sandy':
                                        form = 'wormadam-sandy'
                                    elif form == 'Trash Cloak':
                                        form = 'wormadam-trash'
                                    elif form == 'Sneasel':
                                        form = 'sneasel'
                                    elif form == 'Hisuian Form' and 'sneasel' == pokemon_data['Pokemon']:
                                        form = 'sneasel-hisui'
                                    else:
                                        raise Exception
                                    pokemon = Pokemon.objects.get(name=form)
                                    moveE = Move.objects.get(name=movestr.lower().replace(' ', '-'))
                                    writer.writerow([pokemon.id, 24, moveE.id, 3, None, None, None])
                        else:
                            raise Exception

                else:
                    if pokemon_data['Pokemon'] == 'wormadam':

                        for move in pokemon_data['Forms']['Standard Level Up']:
                            pokemon = Pokemon.objects.get(name='wormadam-plant')
                            moveE = Move.objects.get(name=move['Move'].lower().replace(' ', '-'))
                            writer.writerow([pokemon.id, 24, moveE.id,1,move['Level'], None, move['Mastery']])
                        for move in pokemon_data['Forms']['Level Up - Sandy Cloak']:
                            pokemon = Pokemon.objects.get(name='wormadam-sandy')
                            moveE = Move.objects.get(name=move['Move'].lower().replace(' ', '-'))
                            writer.writerow([pokemon.id, 24, moveE.id,1,move['Level'], None, move['Mastery']])
                        for move in pokemon_data['Forms']['Level Up - Trash Cloak']:
                            pokemon = Pokemon.objects.get(name='wormadam-trash')
                            moveE = Move.objects.get(name=move['Move'].lower().replace(' ', '-'))
                            writer.writerow([pokemon.id, 24, moveE.id, 1,move['Level'], None, move['Mastery']])
                        for move in pokemon_data['Forms']['Shop']:
                            movestr = move['Move'].lower().replace(' ', '-')
                            for form in move['Form']:
                                if form == 'Wormadam':
                                    form = 'wormadam-plant'
                                elif form == 'Sandy':
                                    form = 'wormadam-sandy'
                                elif form == 'Trash Cloak':
                                    form = 'wormadam-trash'
                                else:
                                    raise Exception
                                pokemon = Pokemon.objects.get(name=form)
                                movestr = movestr.lower().replace(' ', '-')
                                print(movestr)
                                moveE = Move.objects.get(name=movestr)
                                writer.writerow([pokemon.id, 24, moveE.id, 3, None, None, None])
                    else:
                        raise Exception

            elif len(pokemon_data['Forms']) == 2 and list(pokemon_data['Forms'].items())[1][0] == 'Standard Level Up':
                pkmname = pokemon_data['Pokemon'].replace(' ', '-')
                if pkmname == 'mimejr.':
                    pkmname = 'mime-jr'
                if pkmname == 'mr.mime':
                    pkmname = 'mr-mime'
                if pkmname == 'basculegion':
                    pkmname = 'basculegion-male'
                if pkmname == 'tornadus':
                    pkmname = 'tornadus-incarnate'
                if pkmname == 'thundurus':
                    pkmname = 'thundurus-incarnate'
                if pkmname == 'landorus':
                    pkmname = 'landorus-incarnate'
                if pkmname == 'enamorus':
                    pkmname = 'enamorus-incarnate'
                if pkmname == 'giratina':
                    pkmname = 'giratina-origin'
                if pkmname == 'shaymin':
                    pkmname = 'shaymin-land'
                print(pkmname)
                pokemon = Pokemon.objects.get(name=pkmname)
                for move in pokemon_data['Forms']['Standard Level Up']:
                    moveE = Move.objects.get(name=move['Move'].lower().replace(' ','-'))
                    writer.writerow([pokemon.id,24,moveE.id,1,move['Level'],None,move['Mastery']])
                for move in pokemon_data['Forms']['Shop']:
                    movestr = move['Move'].lower().replace(' ', '-')
                    moveE = Move.objects.get(name=movestr.lower().replace(' ', '-'))
                    for form in move['Form']:
                        if form == 'Vulpix':
                            form = 'vulpix'
                        elif form == 'Alola Form' and pkmname =='vulpix':
                            form = 'vulpix-alola'
                        elif form == 'Ninetales' and pkmname =='ninetales':
                            form = 'ninetales'
                        elif form == 'Alola Form' and pkmname =='ninetales':
                            form = 'ninetales-alola'
                        elif form == 'Shaymin' and pkmname =='shaymin-land':
                            form = 'shaymin-land'
                        elif form == 'Sky Forme':
                            form = 'shaymin-sky'
                        else:
                            raise Exception
                        pokemon = Pokemon.objects.get(name=form)
                        writer.writerow([pokemon.id, 24, moveE.id, 3, None, None, None])
            elif len(pokemon_data['Forms']) == 2 and list(pokemon_data['Forms'].items())[1][0] == 'Hisuian Form Level Up':
                pokemon = Pokemon.objects.get(name=pokemon_data['Pokemon'] + '-hisui')
                for move in pokemon_data['Forms']['Hisuian Form Level Up']:
                    moveE = Move.objects.get(name=move['Move'].lower().replace(' ', '-'))
                    writer.writerow([pokemon.id, 24, moveE.id,1, move['Level'], None, move['Mastery']])
                for move in pokemon_data['Forms']['Shop']:
                    moveE = Move.objects.get(name=move['Move'].lower().replace(' ', '-'))
                    writer.writerow([pokemon.id, 24, moveE.id, 3,None, None,None])
            elif len(pokemon_data['Forms']) == 2 and list(pokemon_data['Forms'].items())[1][0] == 'Level Up - White-Striped Form':
                pokemon = Pokemon.objects.get(name='basculin-white-striped')
                for move in pokemon_data['Forms']['Level Up - White-Striped Form']:
                    moveE = Move.objects.get(name=move['Move'].lower().replace(' ', '-'))
                    writer.writerow([pokemon.id, 24, moveE.id,1, move['Level'], None, move['Mastery']])
                for move in pokemon_data['Forms']['Shop']:
                    moveE = Move.objects.get(name=move['Move'].lower().replace(' ', '-'))
                    writer.writerow([pokemon.id, 24, moveE.id, 3,None, None,None])
            else:
                raise Exception