from middleware.api.pokepedia import pokemonmoveapi
from middleware.connection.conn import session
from middleware.db import repository
from middleware.exception.exceptions import SectionNotFoundException
from middleware.util.helper import pokemonhelper, generationhelper, specificcasehelper, pokemonmovehelper
from pokedex.db.tables import PokemonMoveMethod, Generation


def handle_machine_pkm_move():
    pokemons = repository.find_pokemon_with_specific_page(1)

    learnmethod = session.query(PokemonMoveMethod).filter(PokemonMoveMethod.identifier == 'machine').one()
    generations = session.query(Generation).all()

    # noinspection PyShadowingBuiltins
    for id, pokemon in pokemons.items():
        for generation in generations:
            if generation.identifier != 'generation-v':
                continue
            if not generationhelper.check_if_pokemon_has_move_availability_in_generation(pokemon, generation):
                return
            if specificcasehelper.is_specific_pokemon_move_case(learnmethod, pokemon, generation):
                return
            steps = pokemonmovehelper.get_steps_by_pokemon_method_and_gen(pokemon, generation, learnmethod)
            for step in range(1, steps + 1):
                pokepedia_pokemon_name = pokemonhelper.find_pokepedia_pokemon_url_name(pokemon)
                try:
                    print(f'Processing {pokepedia_pokemon_name} generation {generationhelper.gen_to_int(generation)}')
                    pokepedia_data = pokemonmoveapi.get_pokemon_moves(pokemon, pokepedia_pokemon_name, generationhelper.gen_to_int(generation),
                                                                      learnmethod.identifier, step)
                except SectionNotFoundException as exc:
                    test = 3


def _get_page(generation: int, name: str):
    if generation < 7:
        page = '{}/G%C3%A9n%C3%A9ration_{}'.format(name.replace('’', '%27').replace('\'', '%27').replace(' ', '_'),
                                                   generation)
    else:
        page = '{}'.format(name.replace('’', '%27').replace('\'', '%27').replace(' ', '_'))
    return page


handle_machine_pkm_move()
