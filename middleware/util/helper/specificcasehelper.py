from middleware.util.helper.pokemonmovehelper import MACHINE_TYPE
from pokedex.db.tables import PokemonMoveMethod, Pokemon, PokemonMove, Generation


def is_specific_pokemon_move_case(method: PokemonMoveMethod, pkm: Pokemon, gen: Generation):
    if method.identifier == MACHINE_TYPE and pkm.identifier == 'mew':
        return True


def filter_dive_pokemon_move_lgfr(moves: list):
    filtered = []
    for pkmmove in moves:
        if pkmmove.move.identifier == 'dive' and pkmmove.version_group.identifier == 'firered-leafgreen':
            continue
        else:
            filtered.append(pkmmove)
    return filtered
