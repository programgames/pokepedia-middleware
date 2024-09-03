from middleware.connection.conn import session
from middleware.util.helper import generationhelper
from middleware.util.helper.pokemonmovehelper import MACHINE_TYPE, EGG_TYPE
from pokeapi.db import util
from pokeapi.db.tables import PokemonMoveMethod, Pokemon, Generation


def is_specific_pokemon_move_case(method: PokemonMoveMethod, pkm: Pokemon, gen: Generation):
    if method.identifier == MACHINE_TYPE and pkm.identifier == 'mew':
        return True
    if method.identifier == EGG_TYPE and generationhelper.gen_to_int(gen) == 1:
        return True


def filter_dive_pokemon_move_lgfr(moves: list):
    # deprecated : use remove_dive_move_lgfr instead()
    filtered = []
    for pkmmove in moves:
        if pkmmove.move.identifier == 'dive' and pkmmove.version_group.identifier == 'firered-leafgreen':
            continue
        else:
            filtered.append(pkmmove)
    return filtered

def remove_dive_move_lgfr(moves: list):
    filtered = []
    for pkmmove in moves:
        if pkmmove.Move.identifier == 'dive' and pkmmove.Move.identifier == 'firered-leafgreen':
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

# https://bulbapedia.bulbagarden.net/wiki/Smoochum_(Pok%C3%A9mon)/Generation_II_learnset#By_leveling_up
def remove_egg_move_exceptions(gen: Generation,pkm: Pokemon,moves: list):
    filtered = []
    for pkmmove in moves:
        if generationhelper.gen_to_int(gen) == 2:
            if pkmmove.Move.identifier == 'charm' and pkm.identifier == 'bulbasaur':
                continue
            elif pkmmove.Move.identifier == 'charm' and pkm.identifier == 'snorlax':
                continue
            elif pkmmove.Move.identifier == 'charm' and pkm.identifier == 'oddish':
                continue
            elif pkmmove.Move.identifier == 'lovely-kiss' and pkm.identifier == 'smoochum':
                continue
            else:
                filtered.append(pkmmove)
        elif generationhelper.gen_to_int(gen) == 4:
            if pkmmove.Move.identifier == 'head-smash' and pkm.identifier == 'nosepass':
                continue
            else:
                filtered.append(pkmmove)
        elif generationhelper.gen_to_int(gen) == 6:
            if pkmmove.Move.identifier == 'ally-switch' and pkm.identifier == 'tyrogue':
                continue
            else:
                filtered.append(pkmmove)
        elif generationhelper.gen_to_int(gen) == 7:
            if pkmmove.Move.identifier == 'punishment' and pkm.identifier == 'murkrow':
                continue
            else:
                filtered.append(pkmmove)
        else:
            filtered.append(pkmmove)
    return filtered