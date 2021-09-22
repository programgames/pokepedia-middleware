from connection.conn import session
from db.repository import *
import handler.pokemonmoveprocessor as pokemonmoveprocessor
from exception import *


def process_pokemon_move(start: int):
    pokemons = find_pokemon_with_specific_page(start)
    learnmethod = session.query(PokemonMoveMethod).filter(PokemonMoveMethod.identifier == 'level-up').one()
    generations = session.query(Generation).all()


    for id, pokemon in pokemons.items():
        for generation in generations:
            try:
                print('processing ' + pokemon.identifier + ' for generation ' + str(generation.id))
                pokemonmoveprocessor.process(generation, learnmethod, pokemon, False)

            except Exception as exc:
                raise UnrecoverableMessageHandlingError(
                    "Error happened for {} generation {}".format(pokemon.identifier,
                                                                 generation.identifier))
