from connection.conn import session
from db.repository import *
import handler.pokemonmoveprocessor as pokemonmoveprocessor
from exception import *


def process_pokemon_move():
    pokemons = find_pokemon_with_specific_page(1)
    learnmethod = session.query(PokemonMoveMethod).filter(PokemonMoveMethod.identifier == 'level-up').one()
    generations = session.query(Generation).all()

    for generation in generations:
        for id, pokemon in pokemons.items():
            try:
                pokemonmoveprocessor.process(generation, learnmethod, pokemon, False)
            except Exception as exc:
                raise UnrecoverableMessageHandlingError(
                    "Error happened for {} generation {}".format(pokemon.identifier,
                                                                 generation.identifier))
