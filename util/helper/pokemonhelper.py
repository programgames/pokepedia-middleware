from pokedex.db.tables import Pokemon, PokemonSpecies
from connection.conn import session
import re


def get_specific_url_name_if_available(pokemon):
    pokemon_identifier = pokemon.identifier

    if pokemon_identifier == 'kyurem-black':
        return 'Kyurem_Noir'
    elif pokemon_identifier == 'kyurem-white':
        return 'Kyurem_Blanc'
    elif pokemon_identifier == 'necrozma-dusk':
        return 'Necrozma_Crinière_du_Couchant'

    elif pokemon_identifier == 'necrozma-dawn':
        return 'Necrozma_Ailes_de_l\'Aurore'

    elif pokemon_identifier == 'necrozma-ultra':
        return 'Ultra-Necrozma'
    else:
        return False


def get_pokepedia_pokemon_url_name(pokemon: Pokemon):
    specific = get_specific_url_name_if_available(pokemon)

    if specific:
        return specific

    specy_name = pokemon.species.name_map('fr')

    if re.match(r'.*alola.*', pokemon.identifier):
        name = '{}_{}'.format(specy_name, 'd\'Alola')
    elif re.match(r'.*galar.*', pokemon.identifier):
        name = '{}_{}'.format(specy_name, 'de_Galar')
    else:
        name = specy_name

    return name.replace(' ', '_').replace('’', '%27d')
