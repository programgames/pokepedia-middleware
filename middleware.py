import argparse
import sys
from dotenv import load_dotenv

from middleware.connection.conn import session
from middleware.db.tables import CacheItem
from middleware.handler import pokemonmovehandler
from middleware.install import installer

load_dotenv()


def main(junk, *argv):
    parser = create_parser()

    if len(argv) <= 0:
        parser.print_help()
        sys.exit()

    args = parser.parse_args(argv)
    args.func(parser, args)


def create_parser():
    """Build and return an ArgumentParser.
    """
    common_parser = argparse.ArgumentParser(add_help=False)
    parser = argparse.ArgumentParser(
        prog='middleware', description=u'Pokepedia middleware',
        parents=[common_parser],
    )
    cmds = parser.add_subparsers(title='commands', metavar='<command>', help='commands')

    cmd_sync_pokemon_level_moves = cmds.add_parser(
        'syncpokemonlevelmoves', help=u'Sync pokemon level moves',
        parents=[common_parser])
    cmd_sync_pokemon_level_moves.add_argument("--start", help="Pokemon number to start synchro", required=True)
    cmd_sync_pokemon_level_moves.add_argument("--gen", help="Specific gen to sync", required=False)
    cmd_sync_pokemon_level_moves.add_argument("-d", "--debug", action="store_true",
                                              help="enable debug")
    cmd_sync_pokemon_level_moves.set_defaults(func=command_sync_pokemon_level_moves)

    cmd_sync_pokemon_machine_moves = cmds.add_parser(
        'syncpokemonmachinemoves', help=u'Sync pokemon machine moves',
        parents=[common_parser])
    cmd_sync_pokemon_machine_moves.add_argument("--start", help="Pokemon number to start synchro", required=True)
    cmd_sync_pokemon_machine_moves.add_argument("--gen", help="Specific gen to sync", required=False)
    cmd_sync_pokemon_machine_moves.add_argument("-d", "--debug", action="store_true",
                                                help="enable debug")
    cmd_sync_pokemon_machine_moves.set_defaults(func=command_sync_pokemon_machine_moves)

    init_command = cmds.add_parser(
        'init', help=u'init project',
        parents=[common_parser])
    init_command.set_defaults(func=command_install)

    clear_cache_command = cmds.add_parser(
        'clearcache', help=u'clear cache',
        parents=[common_parser])
    clear_cache_command.set_defaults(func=command_clear_cache)

    return parser


def command_sync_pokemon_level_moves(parser, args):
    pokemonmovehandler.process_pokemon_move('level-up', int(args.start), int(args.gen) if args.gen else
    None, args.debug)


def command_sync_pokemon_machine_moves(parser, args):
    pokemonmovehandler.process_pokemon_move('machine', int(args.start), int(args.gen) if args.gen else None, args.debug)

def command_clear_cache(parser, args):
    deleted = session.query(CacheItem).delete()
    print(f"{deleted} cache item deleted")


def command_install(parser, args):
    installer.install()


main(*sys.argv)
