from middleware.generator import pokepediapokemonmovegenerator
from pokedex.db.tables import PokemonMoveMethod, Pokemon, Generation

from middleware.util.helper import pokemonhelper, generationhelper
from middleware.util.helper.pokemonmovehelper import LEVELING_UP_TYPE, EGG_TYPE, TUTOR_TYPE, MACHINE_TYPE
from middleware.api.pokepedia import pokemonmoveapi as api, pokepedia_client
from middleware.formatter.database import pokemonlevelmoveformatter
from middleware.comparator import pokemonlevelupmovecomparator


def process(generation: Generation, learn_method: PokemonMoveMethod, pokemon: Pokemon):
    if not generationhelper.check_if_pokemon_has_move_availability_in_generation(pokemon, generation):
        return

    pokepedia_pokemon_name = pokemonhelper.find_pokepedia_pokemon_url_name(pokemon)

    pokepedia_data = _get_pokepedia_moves_by_method(learn_method, pokemon,
                                                    generationhelper.gen_id_to_int(
                                                        generation.identifier), pokepedia_pokemon_name)
    form_order = _format_forms(pokepedia_data)
    database_moves = pokemonlevelmoveformatter.get_formatted_level_up_database_moves(pokemon, generation, learn_method,
                                                                                     form_order)

    if not pokemonlevelupmovecomparator.compare_level_move(pokepedia_data['satanized']['forms'], database_moves,
                                                           form_order):
        print('Error detected for {} , uploading ...'.format(pokepedia_pokemon_name))
        return _generate_and_upload(learn_method, pokemon, generation, database_moves, pokepedia_data,
                                    pokepedia_pokemon_name,
                                    form_order)


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


def _generate_and_upload(learn_method: PokemonMoveMethod, pokemon: Pokemon, gen: Generation, database_moves: dict,
                         pokepedia_data: dict, pokepedia_pokemon_name: str, form_order: dict):
    generated = pokepediapokemonmovegenerator.generate_move_wiki_text(learn_method, pokemon, gen, database_moves,
                                                                      pokepedia_data['satanized'],
                                                                      pokepedia_pokemon_name, form_order)

    pokepedia_client.upload(int(pokepedia_data['section']), pokepedia_data['page'], generated,
                            'Mis a jour des attaques apprises')
    print('Uploading done')


def _format_forms(pokepedia_data: dict) -> dict:
    """
    Handle case when form is followed by a template like Forme Céleste{{Sup|Pt}}{{Sup|HGSS}}
    """
    form_names = list(pokepedia_data['satanized']['forms'].keys())
    formatteds = {}
    for name in form_names:
        temp = name.split('{', 1)
        if len(temp) == 1:
            formatteds[temp[0]] = ''
        else:
            formatteds[temp[0]] = '{' + temp[1]
    return formatteds
