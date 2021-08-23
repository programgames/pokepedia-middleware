from pokedex.db.tables import PokemonMoveMethod

LEVELING_UP_TYPE = 'level-up'
MACHINE_TYPE = 'machine'
EGG_TYPE = 'egg'
TUTOR_TYPE = 'tutor'


def get_pokepedia_invoke_learn_method(move_method: PokemonMoveMethod) -> str:
    english = move_method.identifier
    french = None
    if english == 'level-up':
        french = 'niveau'

    if not french:
        raise RuntimeError('Impossible to translate learn method {} to french'.format(english))

    return french

