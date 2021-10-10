from middleware.connection.conn import session
from middleware.util.helper import generationhelper
from middleware.util.helper.pokemonmovehelper import MACHINE_TYPE, EGG_TYPE
from pokedex.db import util
from pokedex.db.tables import PokemonMoveMethod, Pokemon, PokemonMove, Generation


def is_specific_pokemon_move_case(method: PokemonMoveMethod, pkm: Pokemon, gen: Generation):
    if method.identifier == MACHINE_TYPE and pkm.identifier == 'mew':
        return True
    if method.identifier == EGG_TYPE and generationhelper.gen_to_int(gen) == 1:
        return True


def filter_dive_pokemon_move_lgfr(moves: list):
    filtered = []
    for pkmmove in moves:
        if pkmmove.move.identifier == 'dive' and pkmmove.version_group.identifier == 'firered-leafgreen':
            continue
        else:
            filtered.append(pkmmove)
    return filtered


def is_specific_pokemon_machine_move(pokemon: Pokemon, generation: Generation):
    if generationhelper.gen_to_int(generation) == 3 and pokemon.identifier == 'deoxys-normal':
        return True
    return False


def is_specific_pokemon_form_name(name):
    if name == 'Wimessir mâle':
        return util.get(session, Pokemon, 'indeedee-male')
    elif name == 'Wimessir femelle':
        return util.get(session, Pokemon, 'indeedee-female')
    return None
