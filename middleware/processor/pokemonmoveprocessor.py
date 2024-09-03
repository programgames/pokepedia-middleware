from middleware.errorhandler import pokemonmoveerrorhandler
from middleware.exception.exceptions import PokemonMoveException
from middleware.generator import pokepediapokemonmovegenerator
from middleware.provider.database import pokemonmoveprovider
from pokeapi.db.tables import PokemonMoveMethod, Pokemon, Generation

from middleware.util.helper import pokemonhelper, generationhelper, specificcasehelper, pokemonmovehelper
from middleware.api.pokepedia import pokemonmoveapi, pokepedia_client
from middleware.comparator import pokemonmachinemovecomparator


def process(generation: Generation, learn_method: PokemonMoveMethod, pokemon: Pokemon):
    if not generationhelper.check_if_pokemon_has_move_availability_in_generation(pokemon, generation):
        return
    if specificcasehelper.is_specific_pokemon_move_case(learn_method, pokemon, generation):
        return

    steps = pokemonmovehelper.get_steps_by_pokemon_method_and_gen(pokemon, generation, learn_method)
    for step in range(1, steps + 1):
        pokepedia_pokemon_name = pokemonhelper.find_pokepedia_pokemon_url_name(pokemon)

        try:
            pokepedia_data = _get_pokepedia_moves_by_method(pokemon, learn_method,
                                                            generationhelper.gen_id_to_int(
                                                                generation.identifier), pokepedia_pokemon_name, step)
            form_order = _format_forms(pokepedia_data)

            database_moves = pokemonmoveprovider.get_database_pokemon_moves(pokemon, generation, learn_method,
                                                                            form_order, step)

            if not pokemonmachinemovecomparator.compare_moves(pokepedia_data['satanized']['forms'], database_moves,
                                                              form_order):
                print('Error detected for {} , step {}, uploading ...'.format(pokepedia_pokemon_name, step))
                _generate_and_upload(learn_method, pokemon, generation, database_moves, pokepedia_data,
                                     pokepedia_pokemon_name,
                                     form_order, step)

        except PokemonMoveException as exc:
            pokemonmoveerrorhandler.handlerpokemonmoveerror(exc, pokemon, generation, step,pokepedia_pokemon_name)


def _get_pokepedia_moves_by_method(pokemon: Pokemon, learn_method: PokemonMoveMethod, gen: int,
                                   pokepedia_pokemon_name: str, step: int):
    return pokemonmoveapi.get_pokemon_moves(pokemon, pokepedia_pokemon_name, gen, learn_method.identifier, step)


def _generate_and_upload(learn_method: PokemonMoveMethod, pokemon: Pokemon, gen: Generation, database_moves: dict,
                         pokepedia_data: dict, pokepedia_pokemon_name: str, form_order: dict, step: int):
    generated = pokepediapokemonmovegenerator.generate_move_wiki_text(learn_method, pokemon, gen, database_moves,
                                                                      pokepedia_data['satanized'],
                                                                      pokepedia_pokemon_name, form_order, step)

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
