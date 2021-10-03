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


def vg_id_to_short_name(version_group):
    if version_group == 'red-blue':
        return 'RB'
    elif version_group == 'yellow':
        return 'J'
    elif version_group == 'gold-silver':
        return 'OA'
    elif version_group == 'crystal':
        return 'C'
    elif version_group == 'ruby-sapphire':
        return 'RS'
    elif version_group == 'emerald':
        return 'É'
    elif version_group == 'firered-leafgreen':
        return 'RFVF'
    elif version_group == 'diamond-pearl':
        return 'DP'
    elif version_group == 'platinum':
        return 'Pt'
    elif version_group == 'heartgold-soulsilver':
        return 'HGSS'
    elif version_group == 'black-white':
        return 'NB'
    elif version_group == 'black-2-white-2':
        return 'N2B2'
    elif version_group == 'x-y':
        return 'XY'
    elif version_group == 'omega-ruby-alpha-sapphire':
        return 'ROSA'
    elif version_group == 'sun-moon':
        return 'SL'
    elif version_group == 'ultra-sun-ultra-moon':
        return 'USUL'
    elif version_group == 'lets-go-pikachu-lets-go-eevee':
        return 'LGPE'
    elif version_group == 'sword-shield':
        return 'EB'
    else:
        raise RuntimeError('Unknow shortcut')


def get_vg_string_from_vg_identifiers(specifics_vgs: list) -> str:
    if all(vg in ['diamond-pearl', 'platinum'] for vg in specifics_vgs):
        return 'DPP'
    elif all(vg in ['yellow'] for vg in specifics_vgs):
        return 'J'
    elif all(vg in ['emerald','ruby-sapphire'] for vg in specifics_vgs):
        return 'RSE'
    elif all(vg in ['heartgold-soulsilver'] for vg in specifics_vgs):
        return 'HGSS'
    elif all(vg in ['omega-ruby-alpha-sapphire'] for vg in specifics_vgs):
        return 'ROSA'
    elif all(vg in ['black-white'] for vg in specifics_vgs):
        return 'NB'
    elif all(vg in ['black-2-white-2'] for vg in specifics_vgs):
        return 'N2B2'
    elif all(vg in ['x-y'] for vg in specifics_vgs):
        return 'XY'
    elif all(vg in ['ultra-sun-ultra-moon'] for vg in specifics_vgs):
        return 'USUL'
    else:
        raise RuntimeError('Uknow condition')
