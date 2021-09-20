from connection.conn import session
from pokedex.db.tables import Pokemon, Generation, VersionGroup
import db.repository as repository


def int_to_generation_identifier(integer) -> str:
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
        return 'generation-vii'
    else:
        raise RuntimeError('generation not available for integer ' + integer)


def has_pokemon_availabilities_in_generation(pokemon: Pokemon, generation: Generation) -> bool:
    version_groups_entities = session.query(VersionGroup).filter(VersionGroup.generation_id == generation.id).all()

    availabilities = repository.is_pokemon_available_in_version_groups(pokemon,
                                                                       version_groups_entities)

    return len(availabilities) > 0


def get_gen_number_by_name(generation: str) -> int:
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


def get_version_group_by_gen_and_column(generation: Generation, column: int) -> VersionGroup:
    col1 = {
        '1': 'red-blue',
        '2': 'gold-silver',
        '3': 'ruby-sapphire',
        '4': 'diamond-pearl',
        '5': 'black-white',
        '6': 'x-y',
        '7': 'sun-moon',
        '8': 'sword-shield'
    }
    col2 = {
        '1': 'yellow',
        '2': 'crystal',
        '3': 'emerald',
        '4': 'platinum',
        '5': 'black-2-white-2',
        '6': 'omega-ruby-alpha-sapphire',
        '7': 'ultra-sun-ultra-moon'
    }

    col3 = {
        '3': 'firered-leafgreen',
        '4': 'heartgold-soulsilver',
        '7': 'lets-go',
    }

    if column == 1:
        mapping = col1
    elif column == 2:
        mapping = col2
    else:
        mapping = col3

    return session.query(VersionGroup).filter(
        VersionGroup.identifier == mapping[str(get_gen_number_by_name(generation.identifier))]).one()
