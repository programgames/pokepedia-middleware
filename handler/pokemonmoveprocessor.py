from api.pokepedia.pokemonmoveapi import get_level_moves
from pokedex.db.tables import PokemonMoveMethod
from util.helper.generationhelper import *
from util.helper.movesethelper import LEVELING_UP_TYPE


def process(generation: Generation, learn_method: PokemonMoveMethod, pokemon: Pokemon, retry=True):
    if not has_pokemon_availabilities_in_generation(pokemon, generation):
        return

    pokepediaData = get_pokepedia_moves_by_method(learn_method, pokemon,
                                                  get_gen_number_by_name(
                                                      generation.identifier))


def get_pokepedia_moves_by_method(learn_method: PokemonMoveMethod, pokemon: Pokemon, gen: int):

    medthod_identifier = learn_method.identifier
    if medthod_identifier == LEVELING_UP_TYPE:
        return get_level_moves()
