import logging
import os

from dotenv import load_dotenv
from middleware.db.repository import find_pokemon_with_specific_page
import middleware.processor.pokemonmove.pokemonmoveprocessor as pokemonmoveprocessor
from middleware.exception import MaxChangesReached
from django.db import transaction

from pokeapi.pokemon_v2.models import Generation, MoveLearnMethod

load_dotenv()


def process_pokemon_move(move_method_type: str, start: int, from_gen: int = None,to_gen: int = None, debug: bool = False, max_changes = int):
    logging.basicConfig(filename=os.getenv('LOG_PATH'), level=logging.INFO)

    # Fetch the list of Pokémon with specific pages
    pokemons = find_pokemon_with_specific_page(start)

    # Retrieve the learning method
    try:
        learnmethod = MoveLearnMethod.objects.get(name=move_method_type)
    except MoveLearnMethod.DoesNotExist:
        logging.error(f"Move method {move_method_type} not found.")
        return

    # Retrieve the relevant generations
    if from_gen and to_gen:
        generations = Generation.objects.filter(id__gte=from_gen, id__lte=to_gen)
    else:
        generations = Generation.objects.all()

    try:
        for pokemon_id, pokemon in pokemons.items():
            for generation in generations:
                try:
                    logging.info(f'Processing {pokemon.name} for generation {generation.name} '
                                 f'with ID {pokemon_id} using method {move_method_type}')

                    # Wrap the processing in a transaction to ensure atomicity
                    with transaction.atomic():
                        changed = pokemonmoveprocessor.process(generation, learnmethod, pokemon)
                        if changed:
                            max_changes = max_changes -1
                        if max_changes == 0:
                            raise MaxChangesReached  # Sortir des deux boucles
                except Exception as exc:
                    if isinstance(exc,MaxChangesReached):
                        raise exc
                    logging.error(f"Error processing {pokemon.name} for generation {generation.name}. "
                                  f"Error: {str(exc)}")
                    if debug:
                        raise
    except MaxChangesReached:
        logging.info("Max changes limit reached. Exiting processing.")

