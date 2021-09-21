from pokedex.db.tables import PokemonMoveMethod

from generator.pokepediamovegenerator import generate_move_wiki_text
from util.helper import pokemonhelper
from util.helper.generationhelper import *
from util.helper.movesethelper import LEVELING_UP_TYPE, EGG_TYPE, TUTOR_TYPE, MACHINE_TYPE
from api.pokepedia import pokemonmoveapi as api
from formatter.database import moveformatter
from comparator import levelupmovecomparator


def process(generation: Generation, learn_method: PokemonMoveMethod, pokemon: Pokemon, retry=True):
    if not has_pokemon_availabilities_in_generation(pokemon, generation):
        return


    pokepedia_data= _get_pokepedia_moves_by_method(learn_method, pokemon,
                                                   get_gen_number_by_name(
                                                       generation.identifier))

    database_moves = moveformatter.get_formatted_level_up_database_moves(pokemon, generation, learn_method)

    if not levelupmovecomparator.compare_level_move(database_moves, database_moves):
        return _handle_error(learn_method, pokemon, generation, database_moves,pokepedia_data)


def _get_pokepedia_moves_by_method(learn_method: PokemonMoveMethod, pokemon: Pokemon, gen: int):
    if learn_method.identifier == LEVELING_UP_TYPE:
        return api.get_level_moves(pokemonhelper.find_pokepedia_pokemon_url_name(pokemon), gen)
    elif learn_method.identifier == EGG_TYPE:
        return api.get_egg_moves(pokemonhelper.find_pokepedia_pokemon_url_name(pokemon), gen)
    if learn_method.identifier == TUTOR_TYPE:
        return api.get_tutor_moves(pokemonhelper.find_pokepedia_pokemon_url_name(pokemon), gen)
    if learn_method.identifier == MACHINE_TYPE:
        return api.get_machine_moves(pokemonhelper.find_pokepedia_pokemon_url_name(pokemon), gen)
    else:
        raise RuntimeError('Unknow pokepedia move method : {}'.format(learn_method))


def _handle_error(learn_method: PokemonMoveMethod, pokemon: Pokemon, gen: int, database_moves: list, pokepedia_data: dict):
    generated = generate_move_wiki_text(learn_method, pokemon, gen, database_moves, pokepedia_data)

    # TODO: upload
