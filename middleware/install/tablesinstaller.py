from sqlalchemy.engine.base import Engine

from middleware.db.tables import pokemon_type_past_table
from middleware.db.tables import move_name_changelog_table, pokemon_move_availability_table, \
    pkm_availability_form_table, cache_item_table
from middleware.db.repository import *
from middleware.install import translationinstaller, pokemonmoveavailablityinstaller, pokemontypeinstaller


def create_app_tables():
    engine = session.bind  # type: Engine
    print('Creating tables...')

    move_name_changelog_table_object = move_name_changelog_table.__table__
    pokemon_move_availability_table_object = pokemon_move_availability_table.__table__
    pokemon_type_past_object = pokemon_type_past_table.__table__
    cache_item_table_object = cache_item_table.__table__

    if engine.has_table(MoveNameChangelog.__tablename__):
        move_name_changelog_table_object.drop()
    if engine.has_table(PokemonMoveAvailability.__tablename__):
        pokemon_move_availability_table_object.drop()
    if engine.has_table('pkm_availability_form'):
        pkm_availability_form_table.drop()
    if engine.has_table('pokemon_type_past'):
        pokemon_type_past_object.drop()
    if engine.has_table('cache_item'):
        cache_item_table_object.drop()

    pokemon_move_availability_table_object.create(engine)
    move_name_changelog_table_object.create(engine)
    pkm_availability_form_table.create(engine)
    pokemon_type_past_object.create(engine)
    cache_item_table_object.create(engine)


def fill_app_tables():
    # clean tables before
    print('Filling tables...')
    session.query(MoveNameChangelog).delete()
    session.query(PokemonMoveAvailability).delete()
    session.commit()
    #####
    translationinstaller.load_french_aliases()
    pokemonmoveavailablityinstaller.load_basic_move_availabilities()
    pokemonmoveavailablityinstaller.load_specific_pokemon_move_availabilities()
    pokemontypeinstaller.load_pokemon_type_past()
