from middleware.util.helper import generationhelper
from middleware.util.helper.ormhelper import get_object_or_none
from middleware.util.helper.pokemonmovehelper import MACHINE_TYPE, EGG_TYPE
from pokeapi.pokemon_v2.models import Pokemon, Generation, MoveLearnMethod


def is_specific_pokemon_move_case(method: MoveLearnMethod, pkm: Pokemon, gen: Generation) -> bool:
    return (
            (method.name == MACHINE_TYPE and pkm.name == 'mew') or
            (method.name == EGG_TYPE and generationhelper.gen_to_int(gen) == 1)
    )


def filter_dive_pokemon_move_lgfr(moves: list) -> list:
    # Deprecated: use remove_dive_move_lgfr instead
    return remove_dive_move_lgfr(moves)


def remove_dive_move_lgfr(moves: list) -> list:
    return [pkmmove for pkmmove in moves if not (
            pkmmove.move.name == 'dive' and pkmmove.version_group.name == 'firered-leafgreen'
    )]


def is_specific_pokemon_machine_move(pokemon: Pokemon, generation: Generation) -> bool:
    return generationhelper.gen_to_int(generation) == 3 and pokemon.name == 'deoxys-normal'


def is_specific_pokemon_form_name(name: str) -> Pokemon:
    name_to_identifier = {
        'Wimessir mâle': 'indeedee-male',
        'Wimessir femelle': 'indeedee-female'
    }
    identifier = name_to_identifier.get(name)
    return get_object_or_none(Pokemon, identifier) if identifier else None


def remove_egg_move_exceptions(gen: Generation, pkm: Pokemon, moves: list) -> list:
    exceptions = {
        2: {
            'charm': {'bulbasaur', 'snorlax', 'oddish'},
            'lovely-kiss': {'smoochum'}
        },
        4: {
            'head-smash': {'nosepass'}
        },
        6: {
            'ally-switch': {'tyrogue'}
        },
        7: {
            'punishment': {'murkrow'}
        }
    }

    gen_int = generationhelper.gen_to_int(gen)
    filtered = []

    for pkmmove in moves:
        move_id = pkmmove.move.name
        if gen_int in exceptions and move_id in exceptions[gen_int]:
            if pkm.name in exceptions[gen_int][move_id]:
                continue
        filtered.append(pkmmove)

    return filtered