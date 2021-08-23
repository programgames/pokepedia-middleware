import os

from api.pokepedia.pokemonmoveapiclient import get_pokemon_moves
from satanizer.pokepedialevelmovesatanizer import check_and_sanitize_moves
from util.helper.movesethelper import LEVELING_UP_TYPE


def _get_level_moves_from_cache(name: str, generation: int) -> dict:
    return get_pokemon_moves(name, generation, LEVELING_UP_TYPE)


def get_level_moves(name: str, generation: int) -> dict:
    moves_data = _get_level_moves_from_cache(name, generation)
    moves_data['satanized'] = check_and_sanitize_moves(moves_data['wikitext'])

    return moves_data


def get_raw_wiki_text(name: str, generation: int) -> str:
    formated = _get_level_moves_from_cache(name, generation)
    return os.sep.join(map(str, formated.values()))
