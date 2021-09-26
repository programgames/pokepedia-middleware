from connection.conn import session
from db.repository import *
import handler.pokemonmoveprocessor as pokemonmoveprocessor
from exception import *
from util.helper import generationhelper


def process_pokemon_move(start: int, gen: int,only_download=False):
    pokemons = find_pokemon_with_specific_page(start)
    learnmethod = session.query(PokemonMoveMethod).filter(PokemonMoveMethod.identifier == 'level-up').one()
    if gen:
        generations = session.query(Generation).filter(
            Generation.identifier == generationhelper.int_to_generation_identifier(gen)).all()
    else:
        generations = session.query(Generation).all()

    for id, pokemon in pokemons.items():
        for generation in generations:
            try:
                print('processing ' + pokemon.identifier + ' for generation ' + str(generation.id) + f" with id {pokemon.id}")
                pokemonmoveprocessor.process(generation, learnmethod, pokemon, False,only_download)

            except Exception as exc:
                raise UnrecoverableMessageHandlingError(
                    "Error happened for {} generation {}".format(pokemon.identifier,
                                                                 generation.identifier))
