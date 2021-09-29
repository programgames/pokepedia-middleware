from pokedex.db.tables import PokemonMoveMethod

LEVELING_UP_TYPE = 'level-up'
MACHINE_TYPE = 'machine'
EGG_TYPE = 'egg'
TUTOR_TYPE = 'tutor'

""" Provide tools to deal with pokemon moves
"""


def get_pokepedia_invoke_learn_method(move_method: PokemonMoveMethod) -> str:
    french = None
    if move_method.identifier == LEVELING_UP_TYPE:
        french = 'niveau'
    elif move_method.identifier == MACHINE_TYPE:
        french = 'capsule'

    if not french:
        raise RuntimeError('Impossible to translate learn method {} to french'.format(move_method.identifier))

    return french
