from pokedex.db.tables import PokemonMoveMethod

from generator.pokepediamovegenerator import generate_move_wiki_text
from util.helper import pokemonhelper
from util.helper.generationhelper import *
from util.helper.movesethelper import LEVELING_UP_TYPE, EGG_TYPE, TUTOR_TYPE, MACHINE_TYPE
from api.pokepedia import pokemonmoveapi as api, pokepedia_client
from formatter.database import moveformatter
from comparator import levelupmovecomparator


def process(generation: Generation, learn_method: PokemonMoveMethod, pokemon: Pokemon, retry=True):
    if not has_pokemon_availabilities_in_generation(pokemon, generation):
        return

    pokepedia_pokemon_name = pokemonhelper.find_pokepedia_pokemon_url_name(pokemon)
    pokepedia_data = _get_pokepedia_moves_by_method(learn_method, pokemon,
                                                    get_gen_number_by_identifier(
                                                        generation.identifier), pokepedia_pokemon_name)
    form_order = list(pokepedia_data['satanized']['forms'].keys())
    database_moves = moveformatter.get_formatted_level_up_database_moves(pokemon, generation, learn_method, form_order)

    if not levelupmovecomparator.compare_level_move(pokepedia_data['satanized']['forms'], database_moves):
        return _handle_error(learn_method, pokemon, generation, database_moves, pokepedia_data,pokepedia_pokemon_name)


def _get_pokepedia_moves_by_method(learn_method: PokemonMoveMethod, pokemon: Pokemon, gen: int,
                                   pokepedia_pokemon_name: str):
    if learn_method.identifier == LEVELING_UP_TYPE:
        return api.get_level_moves(pokepedia_pokemon_name, gen)
    elif learn_method.identifier == EGG_TYPE:
        return api.get_egg_moves(pokemonhelper.find_pokepedia_pokemon_url_name(pokemon), gen)
    if learn_method.identifier == TUTOR_TYPE:
        return api.get_tutor_moves(pokemonhelper.find_pokepedia_pokemon_url_name(pokemon), gen)
    if learn_method.identifier == MACHINE_TYPE:
        return api.get_machine_moves(pokemonhelper.find_pokepedia_pokemon_url_name(pokemon), gen)
    else:
        raise RuntimeError('Unknow pokepedia move method : {}'.format(learn_method))


def _handle_error(learn_method: PokemonMoveMethod, pokemon: Pokemon, gen: Generation, database_moves: list,
                  pokepedia_data: dict,pokepedia_pokemon_name: str):
    generated = generate_move_wiki_text(learn_method, pokemon, gen, database_moves, pokepedia_data['satanized'],pokepedia_pokemon_name)

    pokepedia_client.upload(int(pokepedia_data['section']), pokepedia_data['page'], generated,
                            'Mis a jour des attaques apprises')
    print('UPLOAD')
