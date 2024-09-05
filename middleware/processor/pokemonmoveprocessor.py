from middleware.errorhandler import pokemonmoveerrorhandler
from middleware.exception.exceptions import PokemonMoveException
from middleware.generator import pokepediapokemonmovegenerator
from middleware.provider.database import pokemonmoveprovider
from middleware.util.helper import pokemonhelper, generationhelper, specificcasehelper, pokemonmovehelper
from middleware.api.pokepedia import pokemonmoveapi, pokepedia_client
from middleware.comparator import pokemonmachinemovecomparator
from middleware.util.helper.generationhelper import gen_to_int, gen_int_to_name
from pokeapi.pokemon_v2.models import Pokemon, Generation, MoveLearnMethod


def process(generation: Generation, learn_method: MoveLearnMethod, pokemon: Pokemon):
    # Check if the Pokémon has move availability in the generation
    if not generationhelper.check_if_pokemon_has_move_availability_in_generation(pokemon, generation):
        return

    # Check for specific move cases that should be skipped
    if specificcasehelper.is_specific_pokemon_move_case(learn_method, pokemon, generation):
        return

    print(f'Processing {pokemon.name} species id {pokemon.pokemon_species_id} for generation '
          f'with ID {generation.id} using method {learn_method.name} ')
    # Determine the number of steps to process based on the learning method and generation
    steps = pokemonmovehelper.get_steps_by_pokemon_method_and_gen(pokemon, generation, learn_method)
    for step in range(1, steps + 1):
        pokepedia_pokemon_name = pokemonhelper.find_pokepedia_pokemon_url_name(pokemon)

        try:
            # Retrieve and compare Poképedia data with the database data
            pokepedia_data = _get_pokepedia_moves_by_method(pokemon, learn_method, generationhelper.gen_name_to_gen_number(generation.name), pokepedia_pokemon_name, step)
            form_order = _format_forms(pokepedia_data)

            database_moves = pokemonmoveprovider.get_database_pokemon_moves(pokemon, generation, learn_method, form_order, step)

            if not pokemonmachinemovecomparator.compare_moves(pokepedia_data['satanized']['forms'], database_moves, form_order):
                print(f'Error detected for {pokepedia_pokemon_name}, step {step}, uploading ...')
                _generate_and_upload(learn_method, pokemon, generation, database_moves, pokepedia_data, pokepedia_pokemon_name, form_order, step)
                return True

        except PokemonMoveException as exc:
            # Handle errors specific to Pokémon move processing
            pokemonmoveerrorhandler.handlerpokemonmoveerror(exc, pokemon, generation, step, pokepedia_pokemon_name)
    return False


def _get_pokepedia_moves_by_method(pokemon: Pokemon, learn_method: MoveLearnMethod, gen: int, pokepedia_pokemon_name: str, step: int) -> dict:
    return pokemonmoveapi.get_pokemon_moves(pokemon, pokepedia_pokemon_name, gen, learn_method.name, step)


def _generate_and_upload(learn_method: MoveLearnMethod, pokemon: Pokemon, gen: Generation, database_moves: dict, pokepedia_data: dict, pokepedia_pokemon_name: str, form_order: dict, step: int):
    generated = pokepediapokemonmovegenerator.generate_move_wiki_text(learn_method, pokemon, gen, database_moves, pokepedia_data['satanized'], pokepedia_pokemon_name, form_order, step)
    pokepedia_client.upload(int(pokepedia_data['section']), pokepedia_data['page'], generated, 'Mis à jour des attaques apprises')
    print('Uploading done')


def _format_forms(pokepedia_data: dict) -> dict:
    """
    Handle cases where the form name is followed by a template, e.g., Forme Céleste{{Sup|Pt}}{{Sup|HGSS}}
    """
    formatteds = {}
    for name in pokepedia_data['satanized']['forms'].keys():
        split_name = name.split('{', 1)
        formatteds[split_name[0]] = '{' + split_name[1] if len(split_name) > 1 else ''
    return formatteds
