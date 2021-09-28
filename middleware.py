import argparse
import sys
from dotenv import load_dotenv

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

    cmd_sync_pokemon_moves = cmds.add_parser(
        'syncpokemonmoves', help=u'Sync pokemon moves',
        parents=[common_parser])
    cmd_sync_pokemon_moves.add_argument("--start", help="Pokemon number to start synchro", required=True)
    cmd_sync_pokemon_moves.add_argument("--gen", help="Specific gen to sync", required=False)
    cmd_sync_pokemon_moves.add_argument("-d", "--debug", action="store_true",
                        help="enable debug")
    cmd_sync_pokemon_moves.set_defaults(func=command_sync_pokemon_moves)

    init_command = cmds.add_parser(
        'init', help=u'init project',
        parents=[common_parser])
    init_command.set_defaults(func=command_install)

    return parser


def command_sync_pokemon_moves(parser, args):
    pokemonmovehandler.process_pokemon_level_move(int(args.start), int(args.gen) if args.gen else None,
                                                  args.debug)


def command_install(parser, args):
    installer.install()


main(*sys.argv)
