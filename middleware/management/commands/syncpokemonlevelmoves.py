# syncpokemonlevelmoves.py
from django.core.management.base import BaseCommand
from middleware.handler import pokemonmovehandler

class Command(BaseCommand):
    help = 'Sync pokemon level moves'

    def add_arguments(self, parser):
        parser.add_argument("--start", type=int, required=True, help="Pokemon number to start sync")
        parser.add_argument("--gen", type=int, help="Specific gen to sync", required=False)
        parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

    def handle(self, *args, **kwargs):
        start = kwargs['start']
        gen = kwargs.get('gen')
        debug = kwargs.get('debug', False)
        pokemonmovehandler.process_pokemon_move('level-up', start, gen, debug)
