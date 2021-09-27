from db.repository import *
import handler.pokemonmoveprocessor as pokemonmoveprocessor
from util.helper import generationhelper
import logging
from dotenv import load_dotenv
import os

load_dotenv()

def process_pokemon_move(start: int, gen: int, only_download=False):
    logging.basicConfig(filename=os.getenv('LOG_PATH'))
    pokemons = find_pokemon_with_specific_page(start)
    learnmethod = session.query(PokemonMoveMethod).filter(PokemonMoveMethod.identifier == 'level-up').one()
    if gen:
        generations = session.query(Generation).filter(
            Generation.identifier == generationhelper.int_to_generation_identifier(gen)).all()
    else:
        generations = session.query(Generation).all()

    for id, pokemon in pokemons.items():
        for generation in generations:
            # try:
            print('processing ' + pokemon.identifier + ' for generation ' + str(
                generation.id) + f" with id {pokemon.id}")
            pokemonmoveprocessor.process(generation, learnmethod, pokemon, False, only_download)

            # except Exception as exc:
            #     logging.error("Error happened for {} generation {} , error : {}".format(pokemon.identifier,
            #                                                                generation.identifier,exc))

