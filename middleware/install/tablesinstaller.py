from middleware.install import translationinstaller, pokemonmoveavailablityinstaller
from middleware.models import MoveNameChangelog, PokemonMoveAvailability


def fill_app_tables():
    # clean tables before
    print('Filling tables...')
    MoveNameChangelog.objects.all().delete()
    PokemonMoveAvailability.objects.all().delete()
    #####
    translationinstaller.load_french_aliases()
    pokemonmoveavailablityinstaller.load_basic_move_availabilities()
    pokemonmoveavailablityinstaller.load_specific_pokemon_move_availabilities()
