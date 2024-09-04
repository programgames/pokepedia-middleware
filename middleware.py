import argparse
import sys
from dotenv import load_dotenv

from middleware.handler import pokemonmovehandler
from middleware.install import installer
from middleware.models import CacheItem

# Charger les variables d'environnement
load_dotenv()

def main(junk, *argv):
    parser = create_parser()

    if len(argv) <= 0:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args(argv)
    try:
        args.func(args)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def create_parser():
    """Construit et retourne un ArgumentParser."""
    common_parser = argparse.ArgumentParser(add_help=False)
    parser = argparse.ArgumentParser(
        prog='middleware', description='Pokepedia middleware',
        parents=[common_parser],
    )
    cmds = parser.add_subparsers(title='commands', metavar='<command>', help='commands')

    # Ajouter toutes les commandes disponibles
    add_sync_command(cmds, 'syncpokemonlevelmoves', 'Sync pokemon level moves', command_sync_pokemon_moves, 'level-up')
    add_sync_command(cmds, 'syncpokemonmachinemoves', 'Sync pokemon machine moves', command_sync_pokemon_moves, 'machine')
    add_sync_command(cmds, 'syncpokemoneggmoves', 'Sync pokemon egg moves', command_sync_pokemon_moves, 'egg')

    init_command = cmds.add_parser('init', help='Init project', parents=[common_parser])
    init_command.set_defaults(func=command_install)

    clear_cache_command = cmds.add_parser('clearcache', help='Clear cache', parents=[common_parser])
    clear_cache_command.set_defaults(func=command_clear_cache)

    return parser

def add_sync_command(cmds, name, help_text, func, move_type):
    """Ajoute une commande de synchronisation au parser."""
    cmd = cmds.add_parser(name, help=help_text)
    cmd.add_argument("--start", help="Pokemon number to start sync", required=True)
    cmd.add_argument("--gen", help="Specific gen to sync", required=False)
    cmd.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    cmd.set_defaults(func=lambda args: func(args, move_type))

def command_sync_pokemon_moves(args, move_type):
    """Gère la synchronisation des mouvements Pokémon."""
    start = int(args.start)
    gen = int(args.gen) if args.gen else None
    debug = args.debug
    pokemonmovehandler.process_pokemon_move(move_type, start, gen, debug)

def command_clear_cache(args):
    """Efface le cache de la base de données."""
    deleted_count, _ = CacheItem.objects.all().delete()
    print(f"{deleted_count} cache item(s) deleted")

def command_install(args):
    """Installe les composants nécessaires pour le projet."""
    installer.install()

if __name__ == "__main__":
    main(*sys.argv)