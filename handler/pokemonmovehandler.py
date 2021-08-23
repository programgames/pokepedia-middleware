from connection.conn import session
from db.repository import *
import handler.pokemonmoveprocessor as pokemonmoveprocessor
from exception import *


def process_pokemon_move():
    pokemons = find_pokemon_with_specific_page(1)
    learnmethod = session.query(PokemonMoveMethod).filter(PokemonMoveMethod.identifier == 'level-up')
    generations = session.query(Generation).all()

    for generation in generations:
        for pokemon in pokemons:
            try:
                pokemonmoveprocessor.process(generation, learnmethod, pokemon, False)
            except Exception as exc:
                raise UnrecoverableMessageHandlingError(
                    "Error happened for{} generaton {}".format(pokemon.identifier, generation.identifier))from exc
