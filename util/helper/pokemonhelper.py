from connection.conn import session
from pokedex.db.tables import Pokemon, Generation, VersionGroup
import db.repository as repository
import re


def find_pokepedia_pokemon_url_name(pokemon: Pokemon):
    specific = find_pokepedia_specific_name_if_available(pokemon)

    if specific:
        return specific

    specy_name = pokemon.specy.name_map['fr']

    if not specy_name:
        raise RuntimeError('SpecyName not found for pokemon:   {}'.format(pokemon.identifier))

    if re.match(r'.*alola.*', pokemon.identifier):
        name = '{}_{}'.format(specy_name, 'd\'Alola')
    elif re.match(r'.*galar.*', pokemon.identifier):
        name = '{}_{}'.format(specy_name, 'de_Galar')
    else:
        name = specy_name

    return name.replace(' ', '_')


def find_pokepedia_specific_name_if_available(pokemon: Pokemon):
    if pokemon.name == 'kyurem-black':
        return 'Kyurem_Noir'
    elif pokemon.name == 'kyurem-white':
        return 'Kyurem_Blanc'
    elif pokemon.name == 'necrozma-dusk':
        return 'Necrozma_Crinière_du_Couchant'
    elif pokemon.name == 'necrozma-dawn':
        return 'Necrozma_Ailes_de_l\'Aurore'
    elif pokemon.name == 'necrozma-ultra':
        return 'Ultra-Necrozma'

    return False
