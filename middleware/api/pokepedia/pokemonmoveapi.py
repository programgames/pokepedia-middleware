import os

from middleware.api.pokepedia import pokemonmoveapiclient
from middleware.db import repository
from middleware.satanizer import pokepedialevelmovesatanizer
from middleware.util.helper.pokemonmovehelper import LEVELING_UP_TYPE

"""Abstraction of a Pokepedia client to extract pokemon moves data on respective pokemon page
"""


def _get_level_moves_from_cache(name: str, generation: int) -> dict:
    return repository.get_item_from_cache(
        f'pokepedia.wikitext.pokemonmove.{name}.{generation}.{LEVELING_UP_TYPE}',
        lambda: pokemonmoveapiclient.get_pokemon_moves(name, generation, LEVELING_UP_TYPE)
    )


def get_level_moves(name: str, generation: int) -> dict:
    moves_data = _get_level_moves_from_cache(name, generation)
    moves_data['satanized'] = pokepedialevelmovesatanizer.check_and_sanitize_moves(moves_data['wikitext'], name)

    return moves_data


def get_raw_wiki_text(name: str, generation: int) -> str:
    formated = _get_level_moves_from_cache(name, generation)
    return os.sep.join(map(str, formated.values()))
