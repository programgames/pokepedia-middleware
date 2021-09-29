import os

from middleware.api.pokepedia import pokemonmoveapiclient
from middleware.db import repository
from middleware.satanizer import pokepediapokemonmovesatanizer
from middleware.util.helper.pokemonmovehelper import LEVELING_UP_TYPE, MACHINE_TYPE

"""Abstraction of a Pokepedia client to extract pokemon moves data on respective pokemon page
"""


def get_pokemon_moves(name: str, generation: int, method_type: str, step: int) -> dict:
    if method_type == LEVELING_UP_TYPE:
        moves_data = _get_pokemon_moves_from_cache(name, generation, method_type)
        moves_data['satanized'] = pokepediapokemonmovesatanizer.check_and_sanitize_moves(moves_data['wikitext'], name)
    elif method_type == MACHINE_TYPE:
        if step == 1:
            moves_data = _get_pokemon_moves_from_cache(name, generation, method_type)
            moves_data['satanized'] = pokepediapokemonmovesatanizer.check_and_sanitize_moves(moves_data['wikitext'],
                                                                                             name)
        else:
            raise RuntimeError('Not supported')

    else:
        raise RuntimeError(f'learn method not supported {method_type}')
    return moves_data


def _get_pokemon_moves_from_cache(name: str, generation: int, method_type: str, version_group=None, dt=None) -> dict:
    return repository.get_item_from_cache(
        f'pokepedia.wikitext.pokemonmove.{name}.{generation}.{method_type}',
        lambda: pokemonmoveapiclient.get_pokemon_moves(name, generation, method_type, version_group, dt)
    )
