import logging
import os

from dotenv import load_dotenv
from middleware.db.repository import find_pokemon_with_specific_page
import middleware.processor.pokemonmoveprocessor as pokemonmoveprocessor
from middleware.util.helper import generationhelper
from django.db import transaction

from pokeapi.pokemon_v2.models import Generation, MoveLearnMethod

load_dotenv()


def process_pokemon_move(move_method_type: str, start: int, gen: int = None, debug: bool = False):
    logging.basicConfig(filename=os.getenv('LOG_PATH'), level=logging.INFO)

    # Fetch the list of Pokémon with specific pages
    pokemons = find_pokemon_with_specific_page(start)

    # Retrieve the learning method
    try:
        learnmethod = MoveLearnMethod.objects.get(identifier=move_method_type)
    except MoveLearnMethod.DoesNotExist:
        logging.error(f"Move method {move_method_type} not found.")
        return

    # Retrieve the relevant generations
    if gen:
        generations = Generation.objects.filter(identifier=generationhelper.gen_int_to_id(gen))
    else:
        generations = Generation.objects.all()

    for pokemon_id, pokemon in pokemons.items():
        for generation in generations:
            try:
                logging.info(f'Processing {pokemon.name} for generation {generation.identifier} '
                             f'with ID {pokemon_id} using method {move_method_type}')

                # Wrap the processing in a transaction to ensure atomicity
                with transaction.atomic():
                    pokemonmoveprocessor.process(generation, learnmethod, pokemon)

            except Exception as exc:
                logging.error(f"Error processing {pokemon.identifier} for generation {generation.identifier}. "
                              f"Error: {str(exc)}")
                if debug:
                    raise

