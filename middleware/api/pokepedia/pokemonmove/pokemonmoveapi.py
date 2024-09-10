from middleware.api.pokepedia.pokemonmove.pokemon_move_methods import get_moves_from_cache, handle_machine_moves
from middleware.api.pokepedia.pokemonmove.pokemon_move_exceptions_handler import handle_template_not_found
from middleware.exception.exceptions import (
    TemplateNotFoundError,
    UnsupportedException,
)
from middleware.satanizer.pokemonmove import pokepediapokemonmovesatanizer
from middleware.util.helper.pokemonmovehelper import LEVELING_UP_TYPE, MACHINE_TYPE, EGG_TYPE

""" Abstraction of a Pokepedia client to extract Pokémon moves data on respective Pokémon pages. """


def get_pokemon_moves(pokemon, name: str, generation: int, method_type: str, step: int) -> dict:
    if method_type == LEVELING_UP_TYPE:
        moves_data = get_moves_from_cache(step, name, generation, method_type)
    elif method_type == MACHINE_TYPE:
        moves_data = handle_machine_moves(pokemon, name, generation, method_type, step)
    elif method_type == EGG_TYPE:
        moves_data = get_moves_from_cache(step, name, generation, method_type)
    else:
        raise UnsupportedException(f'Learn method not supported: {method_type}')

    try:
        moves_data['satanized'] = pokepediapokemonmovesatanizer.check_and_sanitize_moves(moves_data['wikitext'], name)
    except TemplateNotFoundError as exc:
        handle_template_not_found(exc, method_type, generation, pokemon, moves_data, step)

    return moves_data