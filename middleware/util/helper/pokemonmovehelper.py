from pokedex.db.tables import PokemonMoveMethod, Generation

LEVELING_UP_TYPE = 'level-up'
MACHINE_TYPE = 'machine'
EGG_TYPE = 'egg'
TUTOR_TYPE = 'tutor'

""" Provide tools to deal with pokemon moves
"""


def get_pokepedia_invoke_learn_method(move_method: PokemonMoveMethod, gen: int, step: int) -> str:
    french = None
    if move_method.identifier == LEVELING_UP_TYPE:
        french = 'niveau'
    elif move_method.identifier == MACHINE_TYPE and not (gen == 8 and step == 2):
        french = 'capsule'
    elif move_method.identifier == MACHINE_TYPE and (gen == 8 and step == 2):
        french = 'disque'

    if not french:
        raise RuntimeError('Impossible to translate learn method {} to french'.format(move_method.identifier))

    return french


def get_pokepedia_version_groups_identifiers_for_pkm_machine_by_step(gen: int, step: int):
    if gen == 1:
        return ['red-blue', 'yellow']
    elif gen == 2:
        return ['gold-silver', 'crystal']
    elif gen == 3:
        return ['ruby-sapphire', 'emerald', 'firered-leafgreen']
    elif gen == 4:
        return ['diamond-pearl', 'platinum', 'heartgold-soulsilver']
    elif gen == 5:
        return ['black-white', 'black-2-white-2']
    elif gen == 6:
        return ['x-y', 'omega-ruby-alpha-sapphire']
    elif gen == 7 and step == 1:
        return ['sun-moon', 'ultra-sun-ultra-moon']
    elif gen == 7 and step == 2:
        return ['lets-go-pikachu-lets-go-eevee']
    elif gen == 8:
        return ['sword-shield']
    else:
        raise RuntimeError(f'Unknow condition gen : {gen} / step : {step}')
