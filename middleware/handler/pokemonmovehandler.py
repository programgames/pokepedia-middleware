from middleware.db.repository import *
import middleware.processor.pokemonmoveprocessor as pokemonmoveprocessor
from middleware.util.helper import generationhelper
import logging
from dotenv import load_dotenv
import os

load_dotenv()


def process_pokemon_level_move(start: int, gen: int, debug: bool):
    logging.basicConfig(filename=os.getenv('LOG_PATH'))
    pokemons = find_pokemon_with_specific_page(start)
    learnmethod = session.query(PokemonMoveMethod).filter(PokemonMoveMethod.identifier == 'level-up').one()
    if gen:
        generations = session.query(Generation).filter(
            Generation.identifier == generationhelper.gen_int_to_id(gen)).all()
    else:
        generations = session.query(Generation).all()

    # noinspection PyShadowingBuiltins
    for id, pokemon in pokemons.items():
        for generation in generations:
            if debug:
                print('processing ' + pokemon.identifier + ' for generation ' + str(
                    generation.id) + f" with id {pokemon.id}")
                pokemonmoveprocessor.process(generation, learnmethod, pokemon)
            else:
                try:
                    print('processing ' + pokemon.identifier + ' for generation ' + str(
                        generation.id) + f" with id {pokemon.id}")
                    pokemonmoveprocessor.process(generation, learnmethod, pokemon)

                except Exception as exc:
                    logging.exception(f"Error happened for {pokemon.identifier} generation {generation.identifier} , "
                                      f"error : {exc}")
