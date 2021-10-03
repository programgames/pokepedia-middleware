from middleware.exception.exceptions import SpecificPokemonMachineMoveError
from middleware.generator import pokepediapokemonmovegenerator
from pokedex.db.tables import PokemonMoveMethod, Pokemon, Generation

from middleware.util.helper import pokemonhelper, generationhelper, specificcasehelper
from middleware.util.helper.pokemonmovehelper import LEVELING_UP_TYPE, MACHINE_TYPE
from middleware.api.pokepedia import pokemonmoveapi, pokepedia_client
from middleware.formatter.database import pokemonlevelmoveformatter, pokemonmachinemoveformatter
from middleware.comparator import pokemonmachinemovecomparator


def _get_steps_by_pokemon_method_and_gen(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod) -> \
        int:
    if learn_method.identifier == LEVELING_UP_TYPE:
        return 1
    elif learn_method.identifier == MACHINE_TYPE and 1 <= generationhelper.gen_to_int(generation) <= 6:
        return 1
    elif learn_method.identifier == MACHINE_TYPE and generationhelper.gen_to_int(generation) == 7:
        lgpe = generationhelper.check_if_pokemon_is_available_in_lgpe(pokemon)
        if lgpe:
            return 2
        else:
            return 3
    elif learn_method.identifier == MACHINE_TYPE and generationhelper.gen_to_int(generation) == 8:
        return 2
    else:
        raise RuntimeError('Unknow')  # TODO improve


def process(generation: Generation, learn_method: PokemonMoveMethod, pokemon: Pokemon):
    if not generationhelper.check_if_pokemon_has_move_availability_in_generation(pokemon, generation):
        return
    if specificcasehelper.is_specific_pokemon_move_case(learn_method, pokemon, generation):
        return

    steps = _get_steps_by_pokemon_method_and_gen(pokemon, generation, learn_method)
    for step in range(1, steps + 1):
        pokepedia_pokemon_name = pokemonhelper.find_pokepedia_pokemon_url_name(pokemon)

        try:
            pokepedia_data = _get_pokepedia_moves_by_method(pokemon, learn_method,
                                                            generationhelper.gen_id_to_int(
                                                                generation.identifier), pokepedia_pokemon_name, step)
            form_order = _format_forms(pokepedia_data)
            if learn_method.identifier == LEVELING_UP_TYPE:
                database_moves = pokemonlevelmoveformatter.get_formatted_level_up_database_moves(pokemon, generation,
                                                                                                 learn_method,
                                                                                                 form_order)
            elif learn_method.identifier == MACHINE_TYPE:
                database_moves = pokemonmachinemoveformatter.get_formatted_machine_database_moves(pokemon, generation,
                                                                                                  learn_method,
                                                                                                  form_order, step)
            else:
                raise RuntimeError(f'invalid learn method {learn_method.identifier}')

            if not pokemonmachinemovecomparator.compare_moves(pokepedia_data['satanized']['forms'], database_moves,
                                                              form_order):
                print('Error detected for {} , step {}, uploading ...'.format(pokepedia_pokemon_name, step))
                _generate_and_upload(learn_method, pokemon, generation, database_moves, pokepedia_data,
                                     pokepedia_pokemon_name,
                                     form_order, step)
        except SpecificPokemonMachineMoveError as exc:
            print(f'{pokepedia_pokemon_name},  doesnt not learn any moves, check manually')
            generated = pokepediapokemonmovegenerator.generate_specific_no_pokemon_machine_move_wikitext(pokemon,
                                                                                                         generation,
                                                                                                         step)
            pokepedia_client.upload(exc.additional_data['section'], exc.additional_data['page'], generated,
                                    'Mis a jour des attaques apprises')


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
