# syncpokemonlevelmoves.py
from django.core.management.base import BaseCommand
from middleware.handler.pokemonmove import pokemonmovehandler


class Command(BaseCommand):
    help = 'Sync pokemon level moves'

    def add_arguments(self, parser):
        parser.add_argument("--start", type=int, required=True, help="Pokemon number to start sync")
        parser.add_argument("--from-gen", type=int, help="From specific gen to sync", required=True)
        parser.add_argument("--to-gen", type=int, help="To specific gen to sync", required=True)
        parser.add_argument("--max-changes", type=int, help="Max changes to upload", required=False)
        parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

    def handle(self, *args, **kwargs):
        start = kwargs['start']
        gen_from = kwargs.get('from_gen')
        to_gen = kwargs.get('to_gen')
        max_changes = kwargs['max_changes']
        if not max_changes:
            max_changes = 9999999999999
        debug = kwargs.get('debug', False)
        pokemonmovehandler.process_pokemon_move('level-up', start, gen_from, to_gen, debug, max_changes)
