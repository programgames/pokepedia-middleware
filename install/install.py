from sqlalchemy.engine.base import Engine
import csv

from db.entity.entity import pokemon_type_past, PokemonTypePast
from util.helper.generationhelper import int_to_generation_identifier
import os
import re
from pathlib import Path
from db.entity import move_name_changelog_table, pokemon_move_availability_table, MoveNameChangelog, \
    pkm_availability_form_table
from db.repository import *


def create_app_tables():
    engine = session.bind  # type: Engine

    move_name_changelog_table_object = move_name_changelog_table.__table__
    pokemon_move_availability_table_object = pokemon_move_availability_table.__table__
    pokemon_type_past_object = pokemon_type_past.__table__

    if engine.has_table(MoveNameChangelog.__tablename__):
        move_name_changelog_table_object.drop()
    if engine.has_table(PokemonMoveAvailability.__tablename__):
        pokemon_move_availability_table_object.drop()
    if engine.has_table('pkm_availability_form'):
        pkm_availability_form_table.drop()
    if engine.has_table('pokemon_type_past'):
        pokemon_type_past_object.drop()

    pokemon_move_availability_table_object.create(engine)
    move_name_changelog_table_object.create(engine)
    pkm_availability_form_table.create(engine)
    pokemon_type_past_object.create(engine)


def fill_app_tables():
    # clean tables before
    session.query(MoveNameChangelog).delete()
    session.query(PokemonMoveAvailability).delete()
    session.commit()
    #####
    load_french_aliases()
    load_basic_move_availabilities()
    load_specific_pokemon_move_availabilities()
    load_pokemon_type_past()


def load_pokemon_type_past():
    header = True
    path = Path(__file__).parent / ('data' + os.sep + 'pokemon_type_past.csv')

    with open(path, newline='', encoding='utf-8') as csvfile:
        line = csv.reader(csvfile, delimiter=',')
        for row in line:
            if header:
                header = False
                continue
            pokemon_id = int(row[0])
            generation_id = int(row[1])
            type_id = int(row[2])
            slot = int(row[3])

            type_past = PokemonTypePast()
            type_past.type_id = type_id
            type_past.generation_id = generation_id
            type_past.pokemon_id = pokemon_id
            type_past.slot = slot
            session.add(type_past)
        session.commit()


def load_french_aliases():
    header = True
    path = Path(__file__).parent / ('data' + os.sep + 'french_move_alias.csv')

    with open(path, newline='', encoding='utf-8') as csvfile:
        line = csv.reader(csvfile, delimiter=',')
        french = session.query(Language).filter(Language.identifier == 'fr').one()
        for row in line:
            if header:
                header = False
                continue
            first_gen = int(re.search(r'^\d+', row[2]).group(0))
            second_gen = int(re.search(r'\d+', row[2]).group(0))
            move = session.query(Move).filter(Move.identifier == row[0]).one()
            if not move:
                raise RuntimeError('Move not found : ' + row[0])
            for i in range(first_gen, second_gen):
                generation_identifier = int_to_generation_identifier(i)
                generation = session.query(Generation).filter(Generation.identifier == generation_identifier).one()
                changelog = MoveNameChangelog(
                    language=french.id, move_id=move.id, generation_id=generation.id,
                    name=row[1]
                )
                session.add(changelog)
        session.commit()


def load_basic_move_availabilities():
    red_blue_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'red-blue').one()
    yellow_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'yellow').one()
    gold_silver_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'gold-silver').one()
    crystal_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'crystal').one()
    ruby_sapphir_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'ruby-sapphire').one()
    emerald_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'emerald').one()
    fire_red_leaf_green_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'firered-leafgreen').one()
    diamond_pearl_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'diamond-pearl').one()
    platinum_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'platinum').one()
    heart_gold_soul_silver_vg = session.query(VersionGroup).filter(
        VersionGroup.identifier == 'heartgold-soulsilver').one()
    black_white_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'black-white').one()
    black2_white2_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'black-2-white-2').one()
    xy_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'x-y').one()
    oras_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'omega-ruby-alpha-sapphire').one()
    sun_moon_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'sun-moon').one()
    ultra_sun_ultra_moon_vg = session.query(VersionGroup).filter(
        VersionGroup.identifier == 'ultra-sun-ultra-moon').one()
    lgpe_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'lets-go-pikachu-lets-go-eevee').one()
    sword_shield_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'sword-shield').one()

    save_availabilities(red_blue_vg, 1, 151)
    save_availabilities(yellow_vg, 1, 151)
    save_availabilities(crystal_vg, 1, 251)
    save_availabilities(gold_silver_vg, 1, 251)
    save_availabilities(fire_red_leaf_green_vg, 1, 386)
    save_availabilities(ruby_sapphir_vg, 1, 386)
    save_availabilities(emerald_vg, 1, 386)
    save_availabilities(diamond_pearl_vg, 1, 493)
    save_availabilities(platinum_vg, 1, 493)
    save_availabilities(heart_gold_soul_silver_vg, 1, 493)
    save_availabilities(black_white_vg, 1, 649)
    save_availabilities(black2_white2_vg, 1, 649)
    save_availabilities(xy_vg, 1, 721)
    save_availabilities(oras_vg, 1, 721)
    save_availabilities(sun_moon_vg, 1, 807)
    save_availabilities(ultra_sun_ultra_moon_vg, 1, 807)
    save_alola_pokemons(sun_moon_vg)
    save_alola_pokemons(ultra_sun_ultra_moon_vg)
    save_alola_pokemons(sword_shield_vg, True)
    save_galar_pokemons(sword_shield_vg)
    save_default_gen8_pokemons(sword_shield_vg)
    save_availabilities(lgpe_vg, 1, 151)
    save_availabilities(lgpe_vg, 808, 809)
    save_alola_pokemons(lgpe_vg)


def load_specific_pokemon_move_availabilities():
    diamond_pearl_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'diamond-pearl').one()
    platinum_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'platinum').one()
    heart_gold_soul_silver_vg = session.query(VersionGroup).filter(
        VersionGroup.identifier == 'heartgold-soulsilver').one()
    black_white_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'black-white').one()
    black2_white2_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'black-2-white-2').one()
    xy_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'x-y').one()
    oras_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'omega-ruby-alpha-sapphire').one()
    sun_moon_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'sun-moon').one()
    ultra_sun_ultra_moon_vg = session.query(VersionGroup).filter(
        VersionGroup.identifier == 'ultra-sun-ultra-moon').one()
    sword_shield_vg = session.query(VersionGroup).filter(VersionGroup.identifier == 'sword-shield').one()

    # gen4
    save_pokemon_move_availabilities_with_forms([diamond_pearl_vg, platinum_vg, heart_gold_soul_silver_vg],
                                                'wormadam-plant', ['wormadam-sandy', 'wormadam-trash'])
    save_pokemon_move_availabilities_with_forms([platinum_vg, heart_gold_soul_silver_vg],
                                                'shaymin-land', ['shaymin-sky'])
    # gen 5
    save_pokemon_move_availabilities_with_forms([black_white_vg, black2_white2_vg],
                                                'wormadam-plant', ['wormadam-sandy', 'wormadam-trash'])
    save_pokemon_move_availabilities_with_forms([black_white_vg, black2_white2_vg],
                                                'shaymin-land', ['shaymin-sky'])
    save_pokemon_move_availabilities_with_forms([black2_white2_vg],
                                                'kyurem', ['kyurem-black', 'kyurem-white'])
    # gen6
    save_pokemon_move_availabilities_with_forms([xy_vg, oras_vg],
                                                'wormadam-plant', ['wormadam-sandy', 'wormadam-trash'])
    save_pokemon_move_availabilities_with_forms([xy_vg, oras_vg],
                                                'shaymin-land', ['shaymin-sky'])
    save_pokemon_move_availabilities_with_forms([xy_vg, oras_vg],
                                                'kyurem', ['kyurem-black', 'kyurem-white'])
    save_pokemon_move_availabilities_with_forms([xy_vg, oras_vg],
                                                'hoopa', ['hoopa-unbound'])
    # gen7
    save_pokemon_move_availabilities_with_forms([sun_moon_vg, ultra_sun_ultra_moon_vg],
                                                'wormadam-plant', ['wormadam-sandy', 'wormadam-trash'])
    save_pokemon_move_availabilities_with_forms([sun_moon_vg, ultra_sun_ultra_moon_vg],
                                                'shaymin-land', ['shaymin-sky'])
    save_pokemon_move_availabilities_with_forms([sun_moon_vg, ultra_sun_ultra_moon_vg],
                                                'kyurem', ['kyurem-black', 'kyurem-white'])
    save_pokemon_move_availabilities_with_forms([sun_moon_vg, ultra_sun_ultra_moon_vg],
                                                'hoopa', ['hoopa-unbound'])
    save_pokemon_move_availabilities_with_forms([sun_moon_vg],
                                                'lycanroc-midday', ['lycanroc-midnight'])
    save_pokemon_move_availabilities_with_forms([ultra_sun_ultra_moon_vg],
                                                'lycanroc-midday', ['lycanroc-midnight', 'lycanroc-dusk'])
    save_pokemon_move_availabilities_with_forms([ultra_sun_ultra_moon_vg],
                                                'necrozma', ['necrozma-dusk', 'necrozma-dawn'])
    # gen 8
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'kyurem', ['kyurem-black', 'kyurem-white'])
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'lycanroc-midday', ['lycanroc-midnight', 'lycanroc-dusk'])
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'necrozma', ['necrozma-dusk', 'necrozma-dawn'])
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'toxtricity-amped', ['toxtricity-low-key'])
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'urshifu-single-strike', ['urshifu-rapid-strike'])
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'calyrex', ['calyrex-ice', 'calyrex-shadow'])


def save_pokemon_move_availabilities_with_forms(version_groups: list, original_name: str, forms: list,
                                                specific_page_forms=False):
    with session.no_autoflush:
        for version_group in version_groups:
            original_pokemon_availability = find_availability_by_pkm_and_form(
                original_name, version_group)
            for form in forms:
                form_pokemon = find_pokemon_by_identifier(form)
                availability = PokemonMoveAvailability()
                availability.version_group_id = version_group.id
                availability.pokemon_id = form_pokemon.id
                availability.has_pokepedia_page = specific_page_forms
                availability.is_default = False
                session.add(availability)

                original_pokemon_availability.forms.append(availability)
                session.add(original_pokemon_availability)
                session.commit()


def save_availabilities(version_group, start, end):
    pokemons = find_default_pokemons_in_national_dex(start, end)
    for pokemon in pokemons:
        move_availability = PokemonMoveAvailability()
        move_availability.version_group_id = version_group.id
        move_availability.pokemon_id = pokemon.id
        session.add(move_availability)
    session.commit()


def save_alola_pokemons(version_group, gen8=False):
    excludeds = [
        'rattata-alola', 'raticate-alola', 'geodude-alola', 'graveler-alola', 'golem-alola', 'grimer-alola', 'muk-alola'
    ]

    pokemons = find_alola_pokemons()
    for pokemon in pokemons:
        if gen8:
            if pokemon.identifier in excludeds:
                continue
        move_availability = PokemonMoveAvailability()
        move_availability.version_group_id = version_group.id
        move_availability.pokemon_id = pokemon.id
        move_availability.is_default = False
        session.add(move_availability)
    session.commit()


def save_galar_pokemons(version_group):
    pokemons = find_galar_pokemons()
    for pokemon in pokemons:
        move_availability = PokemonMoveAvailability()
        move_availability.version_group_id = version_group.id
        move_availability.pokemon_id = pokemon.id
        move_availability.is_default = False
        session.add(move_availability)
    session.commit()


def save_default_gen8_pokemons(version_group):
    pokemons = find_default_gen8_pokemons()
    for pokemon in pokemons:
        move_availability = PokemonMoveAvailability()
        move_availability.version_group_id = version_group.id
        move_availability.pokemon_id = pokemon.id
        session.add(move_availability)
    session.commit()


