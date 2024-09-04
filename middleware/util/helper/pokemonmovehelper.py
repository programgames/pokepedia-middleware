from middleware.exception import InvalidConditionException
from middleware.util.helper import generationhelper
from pokeapi.pokemon_v2.models import Pokemon, Generation, MoveLearnMethod

LEVELING_UP_TYPE = 'level-up'
MACHINE_TYPE = 'machine'
EGG_TYPE = 'egg'
TUTOR_TYPE = 'tutor'

""" Provide tools to deal with Pokémon moves
"""


def get_pokepedia_invoke_learn_method(move_method: MoveLearnMethod, gen: int, step: int) -> str:
    if move_method.name == LEVELING_UP_TYPE:
        return 'niveau'
    elif move_method.name == MACHINE_TYPE:
        if gen == 8 and step == 2:
            return 'disque'
        return 'capsule'
    elif move_method.name == EGG_TYPE and gen >= 2:
        return 'reproduction'

    raise InvalidConditionException(f'Impossible to translate learn method {move_method.name} to French')


def get_pokepedia_version_groups_identifiers(gen: int, step: int) -> list:
    groups_by_gen = {
        1: ['red-blue', 'yellow'],
        2: ['gold-silver', 'crystal'],
        3: ['ruby-sapphire', 'emerald', 'firered-leafgreen'],
        4: ['diamond-pearl', 'platinum', 'heartgold-soulsilver'],
        5: ['black-white', 'black-2-white-2'],
        6: ['x-y', 'omega-ruby-alpha-sapphire'],
        7: {1: ['sun-moon', 'ultra-sun-ultra-moon'], 2: ['lets-go-pikachu-lets-go-eevee']},
        8: ['sword-shield'],
    }

    if gen not in groups_by_gen:
        raise InvalidConditionException(f'Unknown condition for gen: {gen} / step: {step}')

    if gen == 7:
        return groups_by_gen[gen].get(step, [])

    return groups_by_gen[gen]


def get_pokepedia_version_groups_identifiers_for_pkm_machine_by_step(gen: int, step: int) -> list:
    return get_pokepedia_version_groups_identifiers(gen, step)


def get_pokepedia_version_groups_identifiers_for_pkm_egg_by_step(gen: int, step: int) -> list:
    return get_pokepedia_version_groups_identifiers(gen, step)


def get_steps_by_pokemon_method_and_gen(pokemon: Pokemon, generation: Generation,
                                        learn_method: MoveLearnMethod) -> int:
    gen_int = generationhelper.gen_to_int(generation)

    if learn_method.name == LEVELING_UP_TYPE:
        return 1
    elif learn_method.name == MACHINE_TYPE:
        if gen_int <= 6:
            return 1
        elif gen_int == 7:
            if generationhelper.check_if_pokemon_is_available_in_lgpe(pokemon):
                return 1 if pokemon.name in {'meltan', 'melmetal'} else 2
            return 1
        elif gen_int == 8:
            return 2
    elif learn_method.name == EGG_TYPE:
        return 1

    raise NotImplementedError(
        f'Step not implemented for learn method {learn_method.name} and generation {gen_int}')

