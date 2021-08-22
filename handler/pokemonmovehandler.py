from sqlalchemy.engine.base import Engine
from pokedex.db.tables import Move, Generation, Language, VersionGroup, PokemonMoveMethod
import csv
from util import generation_helper, session
import os
import re
from pathlib import Path
from db.entity import move_name_changelog_table, pokemon_move_availability_table, \
    PokemonMoveAvailability, MoveNameChangelog, pkm_availability_form_table
from db import pokemon_repository, pokemon_move_availability_repository
import pokemonmoveprocessor
from exception import *


def process_pokemon_move():
    pokemons = pokemon_repository.find_pokemon_with_specific_page(1)
    learnmethod = session.query(PokemonMoveMethod).filter(PokemonMoveMethod.identifier == 'level-up')
    generations = session.query(Generation).all()

    for generation in generations:
        for pokemon in pokemons:
            try:
                pokemonmoveprocessor.process(generation, learnmethod, pokemon, False)
            except Exception as exc:
                raise UnrecoverableMessageHandlingError(
                    "Error happened for{} generaton {}".format(pokemon.identifier, generation.identifier))from exc
