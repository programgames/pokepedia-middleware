import os

from middleware.api.pokepedia import pokemonmoveapiclient
from middleware.db import repository
from middleware.satanizer import pokepediapokemonmovesatanizer
from middleware.util.helper import databasehelper
from middleware.util.helper.pokemonmovehelper import LEVELING_UP_TYPE, MACHINE_TYPE
from pokedex.db.tables import VersionGroup

"""Abstraction of a Pokepedia client to extract pokemon moves data on respective pokemon page
"""


def get_pokemon_moves(name: str, generation: int, method_type: str, step: int) -> dict:
    # TODO short
    if method_type == LEVELING_UP_TYPE:
        moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type)
    elif method_type == MACHINE_TYPE:
        if 1 <= generation <= 6:
            moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type)
        elif generation == 7 and step == 1:
            vg = databasehelper.get(VersionGroup, 'ultra-sun-ultra-moon')  # or sun-moon
            moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type, vg)
        elif generation == 7 and step == 2:
            vg = databasehelper.get(VersionGroup, 'lets-go-pikachu-lets-go-eevee')

            moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type, vg)
        elif generation == 8 and step == 1:
            moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type, None, False)
        elif generation == 8 and step == 2:
            moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type, None, True)

        else:
            raise RuntimeError('Not supported')

    else:
        raise RuntimeError(f'learn method not supported {method_type}')

    moves_data['satanized'] = pokepediapokemonmovesatanizer.check_and_sanitize_moves(moves_data['wikitext'],
                                                                                     name)
    return moves_data


def _get_pokemon_moves_from_cache(step: int, name: str, generation: int, method_type: str, version_group=None, dt=None) -> dict:
    return repository.get_item_from_cache(
        f'pokepedia.wikitext.pokemonmove.step.{step}.{name}.{generation}.{method_type}',
        lambda: pokemonmoveapiclient.get_pokemon_moves(name, generation, method_type, version_group.identifier
        if version_group else None,
                                                       dt)
    )
