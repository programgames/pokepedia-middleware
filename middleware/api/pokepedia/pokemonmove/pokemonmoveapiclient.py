from middleware.api.pokepedia import pokepedia_client
from middleware.db import repository
from middleware.exception.exceptions import (
    NotAvailableError, SectionNotFoundException, MissingOptionException
)
from middleware.util.helper.pokemonmovehelper import TUTOR_TYPE, MACHINE_TYPE, LEVELING_UP_TYPE, EGG_TYPE

""" Pokepedia client implementation to extract Pokémon moves data from respective Pokémon pages. """

def get_pokemon_moves(name: str, generation: int, move_type: str, version_group_identifier=None, dt=None) -> dict:
    if (move_type in {TUTOR_TYPE, MACHINE_TYPE}) and not version_group_identifier and generation == 7:
        raise MissingOptionException('Argument version_group_name is required for {} type'.format(move_type))

    sections = repository.get_item_from_cache(
        'config.section.pokemonmove.{}.{}'.format(name, generation),
        lambda: get_pokemon_move_sections(name, generation)
    )
    section = get_section_index_by_pokemon_move_type_and_generation(move_type, sections, generation,
                                                                    version_group_identifier, dt)

    page = name.replace("’", "%27").replace("'", "%27").replace(" ", "_")
    if generation < 8:
        page = '{}/Génération_{}'.format(page, generation)

    url = ('https://www.pokepedia.fr/api.php?action=parse&format=json&page={page}&prop=wikitext&'
           'errorformat=wikitext&section={section}&disabletoc=1').format(page=page, section=section)
    content = pokepedia_client.parse(url)
    wikitext = content['parse']['wikitext']['*'].split('\n')

    return {
        'wikitext': wikitext,
        'section': section,
        'page': page,
    }


def get_pokemon_move_sections(name: str, generation: int) -> dict:
    page = name.replace("’", "%27").replace("'", "%27").replace(" ", "_")
    if generation < 8:
        page = '{}/G%C3%A9n%C3%A9ration_{}'.format(page, generation)

    sections_url = ('https://www.pokepedia.fr/api.php?action=parse&format=json&page={}&prop=sections&'
                    'errorformat=wikitext&disabletoc=1').format(page)
    return {
        'sections': pokepedia_client.format_section_by_url(sections_url),
        'page': page
    }



def get_section_index_by_pokemon_move_type_and_generation(move_type: str, sections: dict, generation: int,
                                                          version_group_identifier: str = None,
                                                          dt: bool = None) -> int:
    section_paths = sections['sections']

    section_name_mapping = {
        (LEVELING_UP_TYPE, generation <= 7): 'Capacités apprises//Par montée en niveau',
        (LEVELING_UP_TYPE, generation == 8): 'Capacités apprises//Par montée en niveau//Huitième génération',
        (LEVELING_UP_TYPE, generation == 9): 'Capacités apprises//Par montée en niveau//Neuvième génération',
        (MACHINE_TYPE, generation <= 6): 'Capacités apprises//Par CT/CS',
        (MACHINE_TYPE, generation == 7 and version_group_identifier in {'ultra-sun-ultra-moon', 'sun-moon'}):
            'Capacités apprises//Par CT//Pokémon Soleil et Lune et Pokémon Ultra-Soleil et Ultra-Lune',
        (MACHINE_TYPE, generation == 7 and version_group_identifier == 'lets-go-pikachu-lets-go-eevee'):
            "Capacités apprises//Par CT//Pokémon : Let's Go, Pikachu et Let's Go, Évoli",
        (MACHINE_TYPE, generation == 8 and not dt and version_group_identifier in {'sword-shield','the-isle-of-armor','the-crown-tundra'}): "Capacités apprises//Par CT//Huitième génération//Pokémon Épée et Bouclier",
        (MACHINE_TYPE, generation == 9 and not dt and version_group_identifier in {'brilliant-diamond-and-shining-pearl'}): "Capacités apprises//Par CT//Neuvième génération",
        (MACHINE_TYPE, generation == 8 and dt and version_group_identifier in {'sword-shield','the-isle-of-armor','the-crown-tundra'}): "Capacités apprises//Par DT//Huitième génération//Pokémon Épée et Bouclier",
        (MACHINE_TYPE, generation == 8 and dt and version_group_identifier in {'brilliant-diamond-and-shining-pearl'}): "Capacités apprises//Par DT//Huitième génération//Pokémon Diamant Étincelant et Perle Scintillante",
        (EGG_TYPE, 2 <= generation <= 7): "Capacités apprises//Par reproduction",
        (EGG_TYPE, generation == 8 and version_group_identifier in {'sword-shield','the-isle-of-armor','the-crown-tundra'} ): "Capacités apprises//Par reproduction//Huitième génération//Pokémon Épée et Bouclier",
        (EGG_TYPE, generation == 8 and version_group_identifier in {'brilliant-diamond-and-shining-pearl'} ): "Capacités apprises//Par reproduction//Huitième génération//Pokémon Diamant Étincelant et Perle Scintillante",
        (EGG_TYPE, generation == 9 and version_group_identifier in {'brilliant-diamond-and-shining-pearl'} ): "Capacités apprises//Par capacité Œuf//Neuvième génération//Par reproduction",
        (TUTOR_TYPE, generation == 2 and version_group_identifier == 'crystal'): "Capacités apprises//Par Donneur de capacités//Pokémon Cristal",
        (TUTOR_TYPE, 3 <= generation <= 7): "Capacités apprises//Par Donneur de capacités//{}".format(
            _get_version_group_name(version_group_identifier)),
        (TUTOR_TYPE, generation == 8): "Capacités apprises//Par Donneur de capacités//Huitième génération",
        (TUTOR_TYPE, generation == 9): "Capacités apprises//Par Donneur de capacités//Neuvième génération"
    }

    if (move_type == EGG_TYPE and generation == 1) or (move_type == TUTOR_TYPE and generation == 1):
        raise NotAvailableError("{} moves are not available in generation {}".format(move_type, generation))
    if move_type == TUTOR_TYPE and generation == 2 and version_group_identifier != 'crystal':
        raise NotAvailableError("Tutor moves are only available in Crystal version for generation 2")
    if move_type == TUTOR_TYPE and generation == 3 and version_group_identifier == 'ruby-sapphire':
        raise NotAvailableError("Tutor moves are not available in Ruby/Sapphire")

    section_name = section_name_mapping.get((move_type, True))
    if not section_name or section_name not in section_paths.keys():
        raise SectionNotFoundException(
            'Section not found {} / generation {} / vg : {}'.format(section_name, generation, version_group_identifier), {
                'section_not_found': section_name,
                'generation': generation,
                'version_group': version_group_identifier,
                'sections': section_paths,
                'page': "https://www.pokepedia.fr/{}".format(sections['page'])
            })

    return section_paths[section_name]


def _get_version_group_name(version_group_identifier):
    version_group_names = {
        'firered-leafgreen': 'Pokémon Rouge Feu et Vert Feuille',
        'emerald': 'Pokémon Émeraude',
        'platinum': 'Pokémon Platine',
        'heartgold-soulsilver': 'Pokémon Or HeartGold et Argent SoulSilver',
        'black-white': 'Pokémon Noir et Blanc',
        'black-2-white-2': 'Pokémon Noir 2 et Blanc 2',
        'x-y': 'Pokémon X et Y',
        'omega-ruby-alpha-sapphire': 'Pokémon Rubis Oméga et Saphir Alpha'
    }
    return version_group_names.get(version_group_identifier, 'Unknown Version Group')