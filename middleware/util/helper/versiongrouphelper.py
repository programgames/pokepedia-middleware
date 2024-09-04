from django.core.exceptions import ObjectDoesNotExist
from middleware.exception import InvalidConditionException
from middleware.util.helper import generationhelper
from pokemon_v2.models import VersionGroup

""" Provide tools to deal with version groups
"""

def get_version_group_by_gen_and_column(generation, column: int) -> VersionGroup:
    """
    Used in Pokémon level move process
    """
    mappings = {
        1: {
            1: 'red-blue',
            2: 'yellow'
        },
        2: {
            1: 'gold-silver',
            2: 'crystal'
        },
        3: {
            1: 'ruby-sapphire',
            2: 'emerald',
            3: 'firered-leafgreen'
        },
        4: {
            1: 'diamond-pearl',
            2: 'platinum',
            3: 'heartgold-soulsilver'
        },
        5: {
            1: 'black-white',
            2: 'black-2-white-2'
        },
        6: {
            1: 'x-y',
            2: 'omega-ruby-alpha-sapphire'
        },
        7: {
            1: 'sun-moon',
            2: 'ultra-sun-ultra-moon',
            3: 'lets-go-pikachu-lets-go-eevee'
        },
        8: {
            1: 'sword-shield'
        }
    }

    gen_int = generationhelper.gen_id_to_int(generation.identifier)
    try:
        version_group_identifier = mappings[gen_int][column]
        return VersionGroup.objects.get(identifier=version_group_identifier)
    except (KeyError, ObjectDoesNotExist):
        raise InvalidConditionException(f"Version group not found for generation {gen_int} and column {column}")


def vg_id_to_short_name(version_group: str) -> str:
    short_names = {
        'red-blue': 'RB',
        'yellow': 'J',
        'gold-silver': 'OA',
        'crystal': 'C',
        'ruby-sapphire': 'RS',
        'emerald': 'É',
        'firered-leafgreen': 'RFVF',
        'diamond-pearl': 'DP',
        'platinum': 'Pt',
        'heartgold-soulsilver': 'HGSS',
        'black-white': 'NB',
        'black-2-white-2': 'N2B2',
        'x-y': 'XY',
        'omega-ruby-alpha-sapphire': 'ROSA',
        'sun-moon': 'SL',
        'ultra-sun-ultra-moon': 'USUL',
        'lets-go-pikachu-lets-go-eevee': 'LGPE',
        'sword-shield': 'EB'
    }

    if version_group in short_names:
        return short_names[version_group]
    else:
        raise InvalidConditionException(f'Unknown version group shortcut for version group {version_group}')


# https://www.pokepedia.fr/Mod%C3%A8le:Abr%C3%A9viation
def get_vg_string_from_vg_identifiers(specifics_vgs: list) -> str:
    vg_combinations = {
        frozenset(['diamond-pearl', 'platinum']): 'DPP',
        frozenset(['yellow']): 'J',
        frozenset(['red-blue']): 'RB',
        frozenset(['gold-silver']): 'OA',
        frozenset(['emerald', 'ruby-sapphire']): 'RSE',
        frozenset(['heartgold-soulsilver']): 'HGSS',
        frozenset(['omega-ruby-alpha-sapphire']): 'ROSA',
        frozenset(['black-white']): 'NB',
        frozenset(['black-2-white-2']): 'N2B2',
        frozenset(['x-y']): 'XY',
        frozenset(['ultra-sun-ultra-moon']): 'USUL'
    }

    specific_vgs_set = frozenset(specifics_vgs)
    if specific_vgs_set in vg_combinations:
        return vg_combinations[specific_vgs_set]
    else:
        raise InvalidConditionException(f'Version group shortcut not found for these version groups: {specifics_vgs}')
