from middleware.api.pokepedia import pokepedia_client
from middleware.connection.conn import session
from middleware.util.helper import pokemonhelper, generationhelper, specificcasehelper, pokemonmovehelper
from pokedex.db.tables import PokemonMoveMethod, Generation, Pokemon


def handle_machine_pkm_move():
    # pokemons = repository.find_pokemon_with_specific_page(1)

    pokemons = session.query(Pokemon).filter(Pokemon.identifier == 'mightyena').all()
    learnmethod = session.query(PokemonMoveMethod).filter(PokemonMoveMethod.identifier == 'machine').one()
    generations = session.query(Generation).all()

    # noinspection PyShadowingBuiltins
    for pokemon in pokemons:
        for generation in generations:
            if generation.identifier != 'generation-v':
                continue
            if not generationhelper.check_if_pokemon_has_move_availability_in_generation(pokemon, generation):
                return
            if specificcasehelper.is_specific_pokemon_move_case(learnmethod, pokemon, generation):
                return
            steps = pokemonmovehelper.get_steps_by_pokemon_method_and_gen(pokemon, generation, learnmethod)
            pokepedia_pokemon_name = pokemonhelper.find_pokepedia_pokemon_url_name(pokemon)
            sections = pokepedia_client.parse(_get_page(generation, pokepedia_pokemon_name))
            wikitext = sections['parse']['wikitext']
            generated = _generate_sections(wikitext, _get_schema_for_context(pokemon, learnmethod, generation, steps))


def _get_page(generation: Generation, name: str):
    generation = generationhelper.gen_to_int(generation)
    if generation < 7:
        page = '{}/Génération_{}'.format(
            name.replace('’', '%27').replace('\'', '%27').replace(' ', '_'), generation)
        url = f'https://www.pokepedia.fr/api.php?action=parse&format=json&page={page}' \
              f'&prop=wikitext&errorformat=wikitext&section={3}&disabletoc=1'
    else:
        page = name.replace('’', '%27')
        url = f'https://www.pokepedia.fr/api.php?action=parse&format=json&page={page}' \
              f'&prop=wikitext&errorformat=wikitext&section={3}&disabletoc=1'
    return url


def _get_schema_for_context(pokemon: Pokemon, learn_method: PokemonMoveMethod, generation: Generation, steps: int):
    gen = generationhelper.gen_to_int(generation)
    if 2 <= gen <= 6:
        schema = {
            'Capacités apprises': None,
            'Capacités apprises\\Par montée en niveau': 'Capacités apprises',
            'Capacités apprises\\Par CT/CS': 'Capacités apprises',
            'Capacités apprises\\Par reproduction': 'Capacités apprises',
            'Capacités apprises\\Par Donneur de capacités': 'Capacités apprises',
        }
    else:
        raise RuntimeError('Unknown condition')
    return schema


def _generate_sections(wikitext: str, schema: dict):
    for section, parent in schema.items():
        level = section.count('\\')
        tets =3
    pass


handle_machine_pkm_move()
