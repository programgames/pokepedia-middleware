from pokedex.db.tables import PokemonMoveMethod, Pokemon

from db import find_moves_by_pokemon_move_method_and_version_group, find_french_move_by_pokemon_move
from util.helper.generationhelper import get_version_group_by_gen_and_column


def get_formatted_level_up_database_moves(pokemon: Pokemon, generation: int, learn_method: PokemonMoveMethod):
    return _get_move_forms(pokemon, generation, learn_method)


def _get_move_forms(pokemon: Pokemon, generation: int, learn_method: PokemonMoveMethod):
    preformatteds  = {}
    if generation in [3,4,7]:
        columns = 3
    elif generation in [1,2,5,6]:
        columns = 2
    else:
        columns = 1

    for column in range(1,columns):
        moves = find_moves_by_pokemon_move_method_and_version_group(pokemon,learn_method,get_version_group_by_gen_and_column(generation,column))
        for pokemon_move_entity in moves:
            pass
            name = find_french_move_by_pokemon_move_and_generation(pokemon_move_entity,generation)
