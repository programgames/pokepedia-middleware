from middleware.connection.conn import session
from middleware.api.pokepedia import pokemonmoveapiclient
from middleware.db import repository
from middleware.exception.exceptions import TemplateNotFoundError, SpecificPokemonMachineMoveError, UnsupportedException
from middleware.satanizer import pokepediapokemonmovesatanizer
from middleware.util.helper import databasehelper, machinehelper
from middleware.util.helper.pokemonmovehelper import LEVELING_UP_TYPE, MACHINE_TYPE
from pokedex.db.tables import VersionGroup, PokemonMove, Pokemon, PokemonMoveMethod

"""Abstraction of a Pokepedia client to extract pokemon moves data on respective pokemon page
"""


def get_pokemon_moves(pokemon: Pokemon, name: str, generation: int, method_type: str, step: int) -> dict:
    # TODO short
    if method_type == LEVELING_UP_TYPE:
        moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type)
    elif method_type == MACHINE_TYPE:
        if 1 <= generation <= 6:
            moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type)
        elif generation == 7 and step == 1:
            vg = databasehelper.get(VersionGroup, 'ultra-sun-ultra-moon')  # or sun-moon
            moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type, vg)
        elif generation == 7 and step == 2:
            vg = databasehelper.get(VersionGroup, 'lets-go-pikachu-lets-go-eevee')

            moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type, vg)
        elif generation == 8 and step == 1:
            moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type, None, False)
        elif generation == 8 and step == 2:
            moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type, None, True)

        else:
            raise UnsupportedException(f'API for method {method_type} / generation {generation} / step {step} not '
                                       f'supported')

    else:
        raise UnsupportedException(f'learn method not supported {method_type}')

    try:
        moves_data['satanized'] = pokepediapokemonmovesatanizer.check_and_sanitize_moves(moves_data['wikitext'],
                                                                                         name)
    except TemplateNotFoundError as exc:
        if method_type == MACHINE_TYPE:
            machine_method = session.query(PokemonMoveMethod).filter(PokemonMoveMethod.identifier == method_type).one()
            version = repository.find_highest_version_group_by_generation(generation)
            if step == 2 and generation == 8:
                pkmmoves = session.query(PokemonMove) \
                    .filter(PokemonMove.version_group_id == version.id) \
                    .filter(PokemonMove.pokemon_id == pokemon.id) \
                    .filter(PokemonMove.pokemon_move_method_id == machine_method.id) \
                    .all()
                pkmmoves_number = len(
                    [pkmmove for pkmmove in pkmmoves if machinehelper.is_hm(pkmmove.machine, generation)])

            else:
                pkmmoves_number = len(session.query(PokemonMove) \
                                      .filter(PokemonMove.version_group_id == version.id) \
                                      .filter(PokemonMove.pokemon_id == pokemon.id) \
                                      .filter(PokemonMove.pokemon_move_method_id == machine_method.id) \
                                      .all())
            if pkmmoves_number == 0:
                raise SpecificPokemonMachineMoveError(f'{pokemon.identifier} does not learn any moves my machine',
                                                      {'section': moves_data['section'], 'page': moves_data['page'],
                                                       'wikitext': moves_data['wikitext']})
        raise exc
    return moves_data


def _get_pokemon_moves_from_cache(step: int, name: str, generation: int, method_type: str, version_group=None,
                                  dt=None) -> dict:
    return repository.get_item_from_cache(
        f'pokepedia.wikitext.pokemonmove.step.{step}.{name}.{generation}.{method_type}',
        lambda: pokemonmoveapiclient.get_pokemon_moves(name, generation, method_type, version_group.identifier
        if version_group else None, dt))
