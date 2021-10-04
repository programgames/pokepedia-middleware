from middleware.api.pokepedia import pokepedia_client
from middleware.db import repository
from middleware.exception.exceptions import NotAvailableError, SectionNotFoundException
from middleware.util.helper.pokemonmovehelper import TUTOR_TYPE, MACHINE_TYPE, LEVELING_UP_TYPE, EGG_TYPE

"""Pokepedia client implementation to extract pokemon moves data on respective pokemon page
"""


def get_pokemon_moves(name: str, generation: int, move_type: str, version_group_identifier=None, dt=None) -> dict:
    if (move_type == TUTOR_TYPE or move_type == MACHINE_TYPE) \
            and not version_group_identifier and generation == 7:
        raise RuntimeError('argument version_group_name is required for %s type'.format(move_type))

    sections = repository.get_item_from_cache(
        f'pokepedia.section.pokemonmove.{name}.{generation}',
        lambda: get_pokemon_move_sections(name, generation)
    )
    section = get_section_index_by_pokemon_move_type_and_generation(move_type, sections, generation,
                                                                    version_group_identifier, dt)
    if generation < 7:
        page = '{}/Génération_{}'.format(
            name.replace('’', '%27').replace('\'', '%27').replace(' ', '_'), generation)
        url = f'https://www.pokepedia.fr/api.php?action=parse&format=json&page={page}' \
              f'&prop=wikitext&errorformat=wikitext&section={section}&disabletoc=1'
    else:
        page = name.replace('’', '%27')
        url = f'https://www.pokepedia.fr/api.php?action=parse&format=json&page={page}' \
              f'&prop=wikitext&errorformat=wikitext&section={section}&disabletoc=1'
    content = pokepedia_client.parse(url)
    wikitext = content['parse']['wikitext']['*']
    wikitext = wikitext.split('\n')

    return {
        'wikitext': wikitext,
        'section': section,
        'page': page,
    }


def get_pokemon_move_sections(name: str, generation: int) -> dict:
    if generation < 7:
        sections_url = 'https://www.pokepedia.fr/api.php?action=parse&format=json&page={}/G%C3%A9n%C3%A9ration_{}' \
                       '&prop=sections&errorformat=wikitext&disabletoc=1' \
            .format(name.replace('’', '%27').replace('\'', '%27').replace(' ', '_'), generation)
    else:
        sections_url = 'https://www.pokepedia.fr/api.php?action=parse&format=json' \
                       '&page={}&prop=sections&errorformat=wikitext' \
            .format(name.replace('’', '%27').replace('\'', '%27').replace(' ', '_'))

    return pokepedia_client.format_section_by_url(sections_url)


def get_section_index_by_pokemon_move_type_and_generation(move_type: str, sections: dict, generation: int,
                                                          version_group_identifier: str,
                                                          dt: bool) -> int:
    if move_type == LEVELING_UP_TYPE and generation <= 6:
        section_name = 'Capacités apprises//Par montée en niveau'
    elif move_type == LEVELING_UP_TYPE and generation == 7:
        section_name = 'Capacités apprises//Par montée en niveau//Septième génération'
    elif move_type == LEVELING_UP_TYPE and generation == 8:
        section_name = 'Capacités apprises//Par montée en niveau//Huitième génération'
    elif move_type == MACHINE_TYPE and generation <= 6:
        section_name = 'Capacités apprises//Par CT/CS'
    elif move_type == MACHINE_TYPE and generation == 7 and (
            version_group_identifier == "ultra-sun-ultra-moon" or version_group_identifier == "sun-moon"):
        if 'Capacités apprises//Par CT/CS//Septième génération//Pokémon Soleil et Lune et Pokémon Ultra-Soleil et ' \
           'Ultra-Lune' not in sections.keys():
            section_name = 'Capacités apprises//Par CT/CS//Septième génération'  # pokemon not available in lgpe or
            # without moves
        else:
            section_name = 'Capacités apprises//Par CT/CS//Septième génération//Pokémon Soleil et Lune et Pokémon Ultra-Soleil et Ultra-Lune'
    elif move_type == MACHINE_TYPE and generation == 7 and version_group_identifier == "lets-go-pikachu-lets-go-eevee":
        if 'Capacités apprises//Par CT/CS//Septième génération//Pokémon : Let\'s Go, Pikachu et Let\'s Go, ' \
           'Évoli' not in sections.keys():
            section_name = 'Capacités apprises//Par CT/CS//Septième génération'  # pokemon not available in lgpe or
            # without moves
        else:
            section_name = "Capacités apprises//Par CT/CS//Septième génération//Pokémon : Let's Go, Pikachu et Let's Go, Évoli"
    elif move_type == MACHINE_TYPE and generation == 8 and not dt:
        section_name = "Capacités apprises//Par CT/CS//Huitième génération"
    elif move_type == MACHINE_TYPE and generation == 8 and dt:
        section_name = "Capacités apprises//Par DT//Huitième génération"
    elif move_type == EGG_TYPE and generation == 1:
        raise NotAvailableError("egg mooves are not available in gen 1")
    elif move_type == EGG_TYPE and 2 <= generation <= 6:
        section_name = "Capacités apprises//Par reproduction"
    elif move_type == EGG_TYPE and generation == 7:
        section_name = "Capacités apprises//Par reproduction//Septième génération"
    elif move_type == EGG_TYPE and generation == 8:
        section_name = "Capacités apprises//Par reproduction//Huitième génération"
    elif move_type == TUTOR_TYPE and generation == 1:
        raise NotAvailableError("tutor mooves are not available in gen 1")
    elif move_type == TUTOR_TYPE and generation == 2 and version_group_identifier != 'crystal':
        raise NotAvailableError("tutor mooves are only available in crystal version for gen 2")
    elif move_type == TUTOR_TYPE and generation == 2 and version_group_identifier == 'crystal':
        section_name = "Capacités apprises//Par Donneur de capacités//Pokémon Cristal"
    elif move_type == TUTOR_TYPE and generation == 3 and version_group_identifier == 'ruby-sapphire':
        raise NotAvailableError("tutor mooves are not available in ruby/sapphir")
    elif move_type == TUTOR_TYPE and 3 <= generation <= 6:
        section_name = "Capacités apprises//Par Donneur de capacités//{}".format(
            _get_version_group_name(version_group_identifier))
    elif move_type == TUTOR_TYPE and generation == 7:
        section_name = "Capacités apprises//Par Donneur de capacités//Septième génération"
    elif move_type == TUTOR_TYPE and generation == 8:
        section_name = "Capacités apprises//Par Donneur de capacités//Huitième génération"
    else:
        raise RuntimeError('Unknow condition')

    if section_name not in sections.keys():
        raise SectionNotFoundException(
            f'Section not found {section_name} / generation {generation} / vg : {version_group_identifier}',{
                'section_name': section_name,
                'generation': generation,
                'version_group': version_group_identifier
            })

    return sections[section_name]


def _get_version_group_name(version_group_identifier):
    if version_group_identifier == 'firered-leafgreen':
        return 'Pokémon Rouge Feu et Vert Feuille'
    elif version_group_identifier == 'emerald':
        return 'Pokémon Émeraude'
    elif version_group_identifier == 'platinum':
        return 'Pokémon Platine'
    elif version_group_identifier == 'heartgold-soulsilver':
        return 'Pokémon Or HeartGold et Argent SoulSilver'
    elif version_group_identifier == 'black-white':
        return 'Pokémon Noir et Blanc'
    elif version_group_identifier == 'black-2-white-2':
        return 'Pokémon Noir 2 et Blanc 2'
    elif version_group_identifier == 'x-y':
        return 'Pokémon X et Y'
    elif version_group_identifier == 'omega-ruby-alpha-sapphire':
        return 'Pokémon Rubis Oméga et Saphir Alpha'
