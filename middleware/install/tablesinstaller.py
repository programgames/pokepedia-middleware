from data.v2 import clear_table
from middleware.db.repository import *
from middleware.install import translationinstaller, pokemonmoveavailablityinstaller, pokemontypeinstaller


def create_app_tables():
    print('Creating custom tables...')

    clear_table(MoveNameChangelog)
    clear_table(PokemonMoveAvailability)
    clear_table(PokemonMoveAvailability)
    clear_table(PokemonTypePast)
    clear_table(CacheItem)


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
