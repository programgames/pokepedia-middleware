from middleware.connection.conn import session
from middleware.util.helper import generationhelper
from pokedex.db.tables import Generation, VersionGroup

""" Provide tools to deal with version groups
"""


def get_version_group_by_gen_and_column(generation: Generation, column: int) -> VersionGroup:
    """
    Used  in pokemon level move process
    """
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
        '7': 'lets-go-pikachu-lets-go-eevee',
    }

    if column == 1:
        mapping = col1
    elif column == 2:
        mapping = col2
    else:
        mapping = col3

    return session.query(VersionGroup).filter(
        VersionGroup.identifier == mapping[str(generationhelper.gen_id_to_int(generation.identifier))]).one()
