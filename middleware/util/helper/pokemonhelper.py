from middleware.util.helper.languagehelper import get_pokemon_specy_french_name
from pokeapi.pokemon_v2.models import Pokemon

""" Provide tools to deal with Pokémon
"""

SPECIFIC_NAMES = {
    'kyurem-black': 'Kyurem_Noir',
    'kyurem-white': 'Kyurem_Blanc',
    'necrozma-dusk': 'Necrozma_Crinière_du_Couchant',
    'necrozma-dawn': 'Necrozma_Ailes_de_l\'Aurore',
    'necrozma-ultra': 'Ultra-Necrozma',
    'calyrex-ice': 'Sylveroy_Cavalier_du_Froid',
    'calyrex-shadow': 'Sylveroy_Cavalier_d\'Effroi',
}

def find_pokepedia_pokemon_url_name(pokemon: Pokemon) -> str:
    specific = find_pokepedia_pokemon_page_specific_name_if_available(pokemon)
    if specific:
        return specific

    # Assuming languagehelper.french is the identifier for the French language
    species_name = get_pokemon_specy_french_name(pokemon.pokemon_species).replace(' ', '_')

    if not species_name:
        raise RuntimeError(f'Species name not found for Pokémon: {pokemon.name}')

    # Handle regional forms
    if 'alola' in pokemon.name:
        name = f'{species_name}_d\'Alola'
    elif 'galar' in pokemon.name:
        name = f'{species_name}_de_Galar'
    else:
        name = species_name

    return name.replace(' ', '_')


def find_pokepedia_pokemon_page_specific_name_if_available(pokemon: Pokemon) -> str:
    return SPECIFIC_NAMES.get(pokemon.name, '')
