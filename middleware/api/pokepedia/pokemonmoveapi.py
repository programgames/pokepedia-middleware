from django.core.exceptions import ObjectDoesNotExist
from middleware.api.pokepedia import pokemonmoveapiclient
from middleware.db import repository
from middleware.exception.exceptions import (
    TemplateNotFoundError,
    UnsupportedException,
    NoEggMoveLearnAndNoTemplateException,
    MissingMachineMoveTemplateException,
    NoMachineMoveLearnAndNoTemplateException,
    MissingEggMoveTemplateException
)
from middleware.satanizer import pokepediapokemonmovesatanizer
from middleware.util.helper import machinehelper, ormhelper
from middleware.util.helper.pokemonmovehelper import LEVELING_UP_TYPE, MACHINE_TYPE, EGG_TYPE
from pokeapi.pokemon_v2.models import VersionGroup, PokemonMove, MoveLearnMethod

""" Abstraction of a Pokepedia client to extract Pokémon moves data on respective Pokémon pages. """


def get_pokemon_moves(pokemon, name: str, generation: int, method_type: str, step: int) -> dict:
    if method_type == LEVELING_UP_TYPE:
        moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type)
    elif method_type == MACHINE_TYPE:
        moves_data = _handle_machine_moves(pokemon, name, generation, method_type, step)
    elif method_type == EGG_TYPE:
        moves_data = _get_pokemon_moves_from_cache(step, name, generation, method_type)
    else:
        raise UnsupportedException(f'Learn method not supported: {method_type}')

    try:
        moves_data['satanized'] = pokepediapokemonmovesatanizer.check_and_sanitize_moves(moves_data['wikitext'], name)
    except TemplateNotFoundError as exc:
        _handle_template_not_found(exc, method_type, generation, pokemon, moves_data, step)

    return moves_data


def _handle_machine_moves(pokemon, name, generation: int, method_type: str, step: int) -> dict:
    if 1 <= generation <= 6:
        return _get_pokemon_moves_from_cache(step, name, generation, method_type)
    elif generation == 7:
        vg_identifier = 'ultra-sun-ultra-moon' if step == 1 and not pokemon.identifier in ['meltan',
                                                                                           'melmetal'] else 'lets-go-pikachu-lets-go-eevee'
        vg = ormhelper.get_object_or_none(VersionGroup, vg_identifier)
        return _get_pokemon_moves_from_cache(step, name, generation, method_type, vg)
    elif generation == 8:
        return _get_pokemon_moves_from_cache(step, name, generation, method_type, None, dt=(step == 2))
    else:
        raise UnsupportedException(
            f'API for method {method_type} / generation {generation} / step {step} not supported')


def _get_pokemon_moves_from_cache(step: int, name: str, generation: int, method_type: str, version_group=None,
                                  dt=None) -> dict:
    cache_key = f'config.wikitext.pokemonmove.step.{step}.{name}.{generation}.{method_type}'
    return repository.get_item_from_cache(
        cache_key,
        lambda: pokemonmoveapiclient.get_pokemon_moves(
            name, generation, method_type, version_group.identifier if version_group else None, dt
        )
    )


def _handle_template_not_found(exc, method_type, generation, pokemon, moves_data, step):
    try:
        machine_method = MoveLearnMethod.objects.get(identifier=method_type)
        version = repository.find_highest_version_group_by_generation(generation)

        pkmmoves = PokemonMove.objects.filter(
            version_group_id=version.id,
            pokemon_id=pokemon.id,
            pokemon_move_method_id=machine_method.id
        )

        if method_type == MACHINE_TYPE:
            if step == 2 and generation == 8:
                pkmmoves_number = sum(1 for pkmmove in pkmmoves if machinehelper.is_hm(pkmmove.machine, generation))
            else:
                pkmmoves_number = pkmmoves.count()

            if pkmmoves_number == 0:
                raise NoMachineMoveLearnAndNoTemplateException(
                    f'{pokemon.identifier} does not learn any moves by machine',
                    {'section': moves_data['section'], 'page': moves_data['page'], 'wikitext': moves_data['wikitext']}
                )
            else:
                raise MissingMachineMoveTemplateException(
                    f'{pokemon.identifier} is missing a machine move template',
                    {'section': moves_data['section'], 'page': moves_data['page'], 'wikitext': moves_data['wikitext']}
                )

        elif method_type == EGG_TYPE:
            pkmmoves_number = pkmmoves.count()
            if pkmmoves_number == 0:
                raise NoEggMoveLearnAndNoTemplateException(
                    f'{pokemon.identifier} does not learn any moves by reproduction',
                    {'section': moves_data['section'], 'page': moves_data['page'], 'wikitext': moves_data['wikitext']}
                )
            else:
                raise MissingEggMoveTemplateException(
                    f'{pokemon.identifier} is missing an egg move template',
                    {'section': moves_data['section'], 'page': moves_data['page'], 'wikitext': moves_data['wikitext']}
                )
    except ObjectDoesNotExist:
        raise exc
