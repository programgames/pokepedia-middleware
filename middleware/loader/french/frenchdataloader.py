import os
import csv
import re
from distutils.dep_util import newer

import requests
from bs4 import BeautifulSoup
from middleware.api.pokepedia import pokepedia_client
from openai import OpenAI

from middleware.db import repository
from pokeapi.pokemon_v2.models import Ability, AbilityFlavorText, AbilityName, AbilityChange
from pokeapi.pokemon_v2.models import VersionGroup

client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))
GROUP_RGX = r"\[(.*?)\]\{(.*?)\}"
SUB_RGX = r"\[.*?\]\{.*?\}"


def get_pokemon_category(pokemon_name):
    # Remplacer les espaces par des underscores pour que le nom soit correct dans l'URL
    pokemon_name = pokemon_name.replace(' ', '_')

    page = pokemon_name
    url = ('https://www.pokepedia.fr/api.php?action=parse&format=json&page={page}&prop=wikitext&'
           'errorformat=wikitext&section={section}&disabletoc=1').format(page=page, section=0)
    content = pokepedia_client.parse(url)
    wikitext = content['parse']['wikitext']['*'].split('\n')

    for line in wikitext:
        # Rechercher la ligne qui commence par "| catégorie="
        if line.startswith('| catégorie='):
            # Extraire la valeur à droite de "| catégorie="
            return line.split('=')[1].strip()
    return None


def translate(french):
    aiprompt = f"Traduis cette phrase en Français sachant que c'est une description d'un talent pokémon et que ça doit etre le plus représentatif de la phrase original mais en français: {french}"
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": aiprompt
            }
        ]
    )

    response_content = response.choices[0].message.content
    return response_content


def loadmissingenus():
    with open('pokeapi/data/v2/csv/pokemon_species_names.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        names = []
        genus = 'genus'
        for r in reader:
            if r[0] != 'pokemon_species_id':
                if r[3] == '' and r[1] == '5':
                    genus = get_pokemon_category(r[2])
                else:
                    genus = r[3]
            names.append([r[0], r[1], r[2], genus])

    with open('exportcsv/out/species_names.csv', mode='w', newline='', encoding='utf-8') as file2:
        writer = csv.writer(file2)
        writer.writerow(['pokemon_species_id', 'local_language_id', 'name', 'genus'])
        for n in names:
            writer.writerow([n[0], n[1], n[2], n[3]])


def scrub_str(string):
    groups = re.findall(GROUP_RGX, string)
    for group in groups:
        if group[0]:
            sub = group[0]
        else:
            sub = group[1].split(":")
            if len(sub) >= 2:
                sub = sub[1]
            else:
                sub = sub[0]
            sub = sub.replace("-", " ")
        string = re.sub(SUB_RGX, sub, string, 1)
    return string


def loadmissingabilityeffecttext():
    ability_proses = []
    with open('exportcsv/ability_prose.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for r in reader:
            if r[0] == 'ability_id':
                continue
            ability_proses.append(r)
    frs = []
    for ability_prose in ability_proses:
        if ability_prose[1] == '9':
            french_prose = translate(scrub_str(ability_prose[3]))
            short_french_prose = translate(scrub_str(ability_prose[2]))
            print(short_french_prose)
            frs.append([ability_prose[0], 5, short_french_prose, french_prose])

    ability_proses = ability_proses + frs
    sorted_data = sorted(ability_proses, key=lambda x: (int(x[0]), int(x[1])))

    with open('exportcsv/out/pokemon_v2_abilityeffecttext.csv', mode='w', newline='', encoding='utf-8') as file2:
        writer = csv.writer(file2)
        writer.writerow(['ability_id', 'local_language_id', 'short_effect', 'effect'])
        # Écrire les lignes dans le fichier CSV
        for row in sorted_data:
            writer.writerow(row)
    return sorted_data


def loadmissingabilitychanges():
    for abc in Ability.objects.filter(is_main_series=True):
        changed = get_pokemon_ability_changes(abc.name)
        if changed and AbilityChange.objects.filter(ability_id=abc.id) is None:
            raise Exception
    pass


def get_pokemon_ability_changes(ability_name):
    # Formater le nom du talent pour l'URL (remplace les espaces par des tirets)
    formatted_ability_name = ability_name.replace(" ", "-").lower()
    url = f"https://pokemondb.net/ability/{formatted_ability_name}"

    try:
        # Envoyer une requête GET à la page web
        response = requests.get(url)
        response.raise_for_status()  # Vérifier si la requête a réussi

        # Analyser le contenu HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trouver la section <h3>Changes</h3>
        changes_header = soup.find('h3', text='Changes')

        return changes_header

    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP : {http_err}")
    except Exception as err:
        print(f"Erreur : {err}")


def get_full_text(element):
    return ''.join(element.stripped_strings)


def get_pokemon_ability_description(ability_name_fr):
    if ability_name_fr in ["Intimidation", "Fuite", "Météo", "Engrais", "Essaim", "Technicien", "Épine de Fer",
                           "Aquabulle", "Banc", "Talent", "Commandant"]:
        ability_name_fr = ability_name_fr + "_(talent)"
    # Formater le nom du talent pour l'URL (remplacer les espaces par des underscores)
    formatted_ability_name = ability_name_fr.replace(" ", "_").replace('’', '%27')
    section = 5
    if ability_name_fr == 'Épine de Fer':
        section = 8
    if ability_name_fr == 'Dracolère' or ability_name_fr == 'Danseuse' or ability_name_fr == 'Commandant':  # !!!!!!!!!!!!
        section = 4
        formatted_ability_name = 'Folle_Furie'
    url = ('https://www.pokepedia.fr/api.php?action=parse&format=json&page={page}&prop=wikitext&'
           'errorformat=wikitext&section={section}&disabletoc=1').format(page=formatted_ability_name, section=section)
    content = pokepedia_client.parse(url)
    wikitext = content['parse']['wikitext']['*'].split('\n')
    wikitextcopy = wikitext
    descriptions = {}
    i = 0
    for line in wikitext:
        line = line.replace('Jeu', 'jeu').replace(';De ', ';')
        if not line.startswith(';'):
            i = i + 1
            continue
        elif line.startswith(';{{jeu|RS}} à {{jeu|RFVF}}'):
            descriptions['ruby-sapphire/emerald/firered-leafgreen'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|RSE}}'):
            descriptions['ruby-sapphire/emerald'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|RS}} et {{jeu|firered-leafgreen}}'):
            descriptions['ruby-sapphire/firered-leafgreen'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|RS}} à {{jeu|ROSA}}'):
            descriptions[
                'ruby-sapphire/emerald/firered-leafgreen/diamond-pearl/black-white/black-2-white-2/xy/omega-ruby-alpha-sapphire'] = \
            wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|NB}} à {{jeu|ROSA}}'):
            descriptions['black-white/black-2-white-2/xd/omega-ruby-alpha-sapphire'] = wikitextcopy[i + 1].replace(':',
                                                                                                                   '')
        elif line.startswith(';{{jeu|NB}} et {{jeu|N2B2}}'):
            descriptions['black-white/black-2-white-2'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|DP}} à {{jeu|HGSS}}') or line.startswith(';{{jeu|DPP}} et {{jeu|HGSS}}'):
            descriptions['diamond-pearl/platinum/heartgold-soulsilver'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|SL}} à {{jeu|EB}}'):
            descriptions['sun-moon/ultra-sun-ultra-moon/sword-shield'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|EB}} et {{jeu|EV}}'):
            descriptions['sword-shield/scarlet-violet'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith('Pokémon Soleil et Lune à Pokémon Écarlate et Violet'):
            descriptions['sun-moon/ultra-sun-ultra-moon/sword-shield/scarlet-violet'] = wikitextcopy[i + 1].replace(':',
                                                                                                                    '')
        elif line.startswith(';{{jeu|DP}} à {{jeu|N2B2}}'):
            descriptions['diamond-pearl/platinum/heartgold-soulsilver/black-white/black-2-white-2'] = wikitextcopy[
                i + 1].replace(':', '')
        elif line.startswith(';{{jeu|DP}} à {{jeu|ROSA}}'):
            descriptions[
                'diamond-pearl/platinum/heartgold-soulsilver/black-white/black-2-white-2/xd/omega-ruby-alpha-sapphire'] = \
            wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|DP}} et {{jeu|ROSA}}'):
            descriptions['diamond-pearl/platinum/omega-ruby-alpha-sapphire'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|EV}}') or line.startswith(';{{jeu|EV}}'):
            descriptions['scarlet-violet'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|DP}} à {{jeu|EV}}'):
            descriptions[
                'diamond-pearl/platinum/heartgold-soulsilver/black-white/black-2-white-2/xd/omega-ruby-alpha-sapphire/sun-moon/ultra-sun-ultra-moon/sword-shield/scarlet-violet'] = \
            wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|DP}} à {{jeu|ROSA}}'):
            descriptions[
                'diamond-pearl/platinum/heartgold-soulsilver/black-white/black-2-white-2/xd/omega-ruby-alpha-sapphire/sun-moon/ultra-sun-ultra-moon/sword-shield/scarlet-violet'] = \
            wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|DP}} à {{jeu|EB}}'):
            descriptions[
                'diamond-pearl/platinum/heartgold-soulsilver/black-white/black-2-white-2/xd/omega-ruby-alpha-sapphire/sun-moon/ultra-sun-ultra-moon/sword-shield'] = \
            wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|SL}} à {{jeu|USUL}}') or line.startswith(';{{jeu|SL}} et {{jeu|USUL}}'):
            descriptions['sun-moon/ultra-sun-ultra-moon'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|XY}} à {{jeu|ROSA}}'):
            descriptions['xy/omega-ruby-alpha-sapphire'] = wikitextcopy[i + 1].replace(':', '')
        elif line == ';{{jeu|EB}}':
            descriptions['sword-shield'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|SL}} à {{jeu|EV}}'):
            descriptions['sun-moon/ultra-sun-ultra-moon/xy/omega-ruby-alpha-sapphire/sword-shield/scarlet-violet'] = \
            wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|SL}} à {{jeu|DEPS}}'):
            descriptions['sun-moon/ultra-sun-ultra-moon/xy/omega-ruby-alpha-sapphire/sword-shield'] = wikitextcopy[
                i + 1].replace(':', '')
        elif line.startswith(';{{jeu|XY}} et {{jeu|ROSA}}'):
            descriptions['xy/omega-ruby-alpha-sapphire'] = wikitextcopy[i + 1].replace(':', '')
        elif line.startswith(';{{jeu|PDMTO}}') or line.startswith(
                ';{{jeu|PDMRB}} et {{jeu|PDMTOC}}') or line.startswith(';{{jeu|PDMPI}}') or line.startswith(
                ';{{jeu|PMDM}}') or line.startswith(';{{jeu|PDMRB}}') or line.startswith(';{{jeu|PDMTOC}}'):
            i += 1
            continue
        else:
            raise Exception
        i = i + 1

    return descriptions


def loadmissingfrenchabilityflavors():
    abilities = AbilityName.objects.filter(ability__is_main_series=True, language_id=5)
    french_descs = {}
    post_processed = []
    i = 0
    for ability_name in abilities:
        print(i)
        i += 1
        cache_key = f'ability.{ability_name.name}'

        french_descs[ability_name.name] = repository.get_item_from_cache(
            cache_key,
            lambda: get_pokemon_ability_description(ability_name.name)
        )

    for ability_name in abilities:
        french_desc = french_descs[ability_name.name]
        for vgspack, desc in french_desc.items():
            tableau = vgspack.split('/')
            for vg in tableau:
                if AbilityFlavorText.objects.filter(ability_id=ability_name.ability.id, language_id=5,
                                                    version_group__name=vg) is None:
                    pass
                else:
                    if vg == 'xy':
                        vg = 'x-y'
                    vge = VersionGroup.objects.get(name=vg)
                    post_processed.append([ability_name.ability.id, vge.id, 5, desc])

    with open('exportcsv/out/ability_flavor_text.csv', newline='',mode='w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ability_id', 'version_group_id', 'language_id', 'flavor_text'])
        for l in post_processed:
            writer.writerow(l)


def loadmissingfrenchabilityflavorsgen9():
    csv_file = 'Txt/abilities.csv'
    frs = []

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row[0] == 'ability_id':
                continue
            frs.append([row[0],row[1]])

    news = []
    for row in frs:
        ab = AbilityName.objects.filter(name=row[0], language_id=5).first()
        if not ab:
            print(row[0])
            raise Exception
        trad = AbilityFlavorText.objects.filter(ability=ab.ability, language_id=5,version_group__id=25)
        if trad:
            trad = trad.first()
        if not trad:
            news.append([ab.ability.id,25,5,row[1]])
        else:
            print(" OK pour " + ab.name)
    with open('exportcsv/out/fr.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['ability_id', 'version_group_id', 'language_id', 'flavor_text'])
        # Écrire chaque ligne dans le fichier CSV
        for row in news:
            writer.writerow(row)
def loadermissingfrenchdata():
    # loadmissingenus()
    # loadmissingabilityeffecttext()
    # loadmissingabilitychanges()
    # loadmissingfrenchabilityflavors()
    loadmissingfrenchabilityflavorsgen9()
