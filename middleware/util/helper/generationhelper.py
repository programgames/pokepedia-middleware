from django.core.exceptions import ObjectDoesNotExist
from middleware.exception import InvalidConditionException
import middleware.db.repository as repository
from pokeapi.pokemon_v2.models import Generation, VersionGroup, Pokemon

""" Provide tools to deal with generations
"""



def gen_int_to_id(integer) -> str:
    if integer == 1:
        return 'generation-i'
    elif integer == 2:
        return 'generation-ii'
    elif integer == 3:
        return 'generation-iii'
    elif integer == 4:
        return 'generation-iv'
    elif integer == 5:
        return 'generation-v'
    elif integer == 6:
        return 'generation-vi'
    elif integer == 7:
        return 'generation-vii'
    elif integer == 8:
        return 'generation-viii'
    else:
        raise InvalidConditionException('generation not available for integer ' + integer)


def gen_name_to_gen_number(generation: str) -> int:
    mapping = {
        'generation-i': 1,
        'generation-ii': 2,
        'generation-iii': 3,
        'generation-iv': 4,
        'generation-v': 5,
        'generation-vi': 6,
        'generation-vii': 7,
        'generation-viii': 8,
    }

    return mapping[generation]


def gen_to_int(generation: Generation) -> int:
    mapping = {
        'generation-i': 1,
        'generation-ii': 2,
        'generation-iii': 3,
        'generation-iv': 4,
        'generation-v': 5,
        'generation-vi': 6,
        'generation-vii': 7,
        'generation-viii': 8,
    }

    return mapping[generation.name]


def check_if_pokemon_has_move_availability_in_generation(pokemon: Pokemon, generation: Generation) -> bool:
    version_groups = VersionGroup.objects.filter(generation=generation)
    availabilities = repository.is_pokemon_available_in_version_groups(pokemon, version_groups)
    return availabilities.exists()


def check_if_pokemon_is_available_in_lgpe(pokemon: Pokemon) -> bool:
    try:
        version_group = VersionGroup.objects.get(identifier='lets-go-pikachu-lets-go-eevee')
    except ObjectDoesNotExist:
        return False

    availabilities = repository.is_pokemon_available_in_version_groups(pokemon, [version_group])
    return availabilities.exists()
