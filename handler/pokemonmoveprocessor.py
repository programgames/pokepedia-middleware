from sqlalchemy.engine.base import Engine
from pokedex.db.tables import Move, Generation, Language, VersionGroup, PokemonMoveMethod, Pokemon
import csv
from util import generation_helper, move_set_helper, session
import os
import re
from pathlib import Path
from db.entity import move_name_changelog_table, pokemon_move_availability_table, \
    PokemonMoveAvailability, MoveNameChangelog, pkm_availability_form_table
from db import pokemon_repository, pokemon_move_availability_repository


class PokemonMoveProcessor:
    def __init(self):
        pass

    def process(self, generation: Generation, learn_method: PokemonMoveMethod, pokemon: Pokemon, retry=True):
        if not generation_helper.has_pokemon_availabilities_in_generation(pokemon, generation):
            return

        pokepediaData = self.get_pokepedia_moves_by_method(learn_method, pokemon,
                                                           generation_helper.get_gen_number_by_name(
                                                               generation.identifier))

    def get_pokepedia_moves_by_method(self, learn_method: PokemonMoveMethod, pokemon: Pokemon, gen: int):

        if learn_method.identifier == move_set_helper.LEVELING_UP_TYPE
            return
