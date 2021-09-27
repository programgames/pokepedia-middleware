from pokedex.db.tables import Pokemon
import re

from util.helper import languagehelper


def find_pokepedia_pokemon_url_name(pokemon: Pokemon):
    specific = find_pokepedia_specific_name_if_available(pokemon)

    if specific:
        return specific

    specy_name = pokemon.species.name_map[languagehelper.french]

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
    if pokemon.identifier == 'kyurem-black':
        return 'Kyurem_Noir'
    elif pokemon.identifier == 'kyurem-white':
        return 'Kyurem_Blanc'
    elif pokemon.identifier == 'necrozma-dusk':
        return 'Necrozma_Crinière_du_Couchant'
    elif pokemon.identifier == 'necrozma-dawn':
        return 'Necrozma_Ailes_de_l\'Aurore'
    elif pokemon.identifier == 'necrozma-ultra':
        return 'Ultra-Necrozma'
    elif pokemon.identifier == 'calyrex-ice':
        return 'Sylveroy_Cavalier_du_Froid'
    elif pokemon.identifier == 'calyrex-shadow':
        return 'Sylveroy Cavalier d\'Effroi'

    return False
