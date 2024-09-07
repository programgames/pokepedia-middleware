import os

from pyexpat.errors import messages
import csv
from middleware.api.pokepedia import pokepedia_client
from pokeapi.pokemon_v2.models import PokemonSpeciesName,AbilityEffectText
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))

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


def translate_to_python(french):

   aiprompt = f"Traduis cette phrase en Français sachant que c'est une description d'un talent pokémon et que ça doit etre le plus représentatif de la phrase original mais en français: {french}"
   response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=500,
        messages = [
            {
            "role": "user",
            "content": aiprompt
            }
        ]
    )

   response_content = response.choices[0].message.content
   return response_content


def loadmissingenus():
    for spname in PokemonSpeciesName.objects.all():
        if spname.language.id == 5 and not spname.genus:
            genus = get_pokemon_category(spname.name)
            if not genus:
                raise Exception("No genus found for " + spname.name)
            print(f"spname: {spname.name}, Genus: {genus}")
            spname.genus = genus
            spname.save()


def loadmissingabilityeffecttext():
    abs = []
    with open('exportcsv/pokemon_v2_abilityeffecttext.csv', mode='r') as file:
        reader = csv.reader(file)
        for r in reader:
            if r[0] == 'id':
                continue
            abs.append(r)
    sorted_data = sorted(abs, key=lambda x: (x[3], x[4]))
    for i in range(len(sorted_data)):
        sorted_data[i][0] = i+1  # Mettre la valeur de i dans la première colonne (index 0)

    with open('exportcsv/out/pokemon_v2_abilityeffecttext.csv', mode='w', newline='') as file2:
        writer = csv.writer(file2)

        # Écrire les lignes dans le fichier CSV
        for row in sorted_data:
            writer.writerow(row)

    return sorted_data

    # for text in AbilityEffectText.objects.filter(language=9):
    #     fr = translate_to_python(text.effect)
    #     shortfr = translate_to_python(text.short_effect)
    #     neweffecttext = AbilityEffectText()
    #     neweffecttext.effect = fr
    #     neweffecttext.short_effect = shortfr
    #     neweffecttext.ability = text.ability
    #     neweffecttext.language_id = 5
    #     neweffecttext.save()


def loadermissingfrenchdata():
    # loadmissingenus()
    loadmissingabilityeffecttext()

