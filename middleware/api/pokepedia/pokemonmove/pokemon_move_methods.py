from middleware.api.pokepedia.pokemonmove import pokemonmoveapiclient
from middleware.db import repository
from middleware.exception import UnsupportedException
from middleware.util.helper import ormhelper
from pokeapi.pokemon_v2.models import VersionGroup


def get_moves_from_cache(step: int, name: str, generation: int, method_type: str, version_group=None, dt=None) -> dict:
    cache_key = f'config.wikitext.pokemonmove.step.{step}.{name}.{generation}.{method_type}'
    return repository.get_item_from_cache(
        cache_key,
        lambda: pokemonmoveapiclient.get_pokemon_moves(
            name, generation, method_type, version_group.name if version_group else None, dt
        )
    )

def handle_machine_moves(pokemon, name, generation: int, method_type: str, step: int) -> dict:
    if 1 <= generation <= 6:
        return get_moves_from_cache(step, name, generation, method_type)
    elif generation == 7:
        vg_identifier = 'ultra-sun-ultra-moon' if step == 1 and not pokemon.name in ['meltan',
                                                                                           'melmetal'] else 'lets-go-pikachu-lets-go-eevee'
        vg = ormhelper.get_object_or_none(VersionGroup, vg_identifier)
        return get_moves_from_cache(step, name, generation, method_type, vg)
    elif generation == 8:
        return get_moves_from_cache(step, name, generation, method_type, None, dt=(step == 2))
    else:
        raise UnsupportedException(
            f'API for method {method_type} / generation {generation} / step {step} not supported')