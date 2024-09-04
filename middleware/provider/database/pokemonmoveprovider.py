from middleware.formatter.database import (
    pokemonlevelmoveformatter,
    pokemonmachinemoveformatter,
    pokemoneggmoveformatter
)
from middleware.util.helper.pokemonmovehelper import LEVELING_UP_TYPE, MACHINE_TYPE, EGG_TYPE
from pokeapi.pokemon_v2.models import Pokemon, Generation, MoveLearnMethod


def get_database_pokemon_moves(pokemon: Pokemon, generation: Generation, learn_method: MoveLearnMethod,
                               form_order: dict, step: int):
    """
    Retrieve and format Pokémon moves from the database based on the learning method.
    """
    if learn_method.name == LEVELING_UP_TYPE:
        return pokemonlevelmoveformatter.get_formatted_level_up_database_moves(
            pokemon, generation, learn_method, form_order
        )
    elif learn_method.name == MACHINE_TYPE:
        return pokemonmachinemoveformatter.get_formatted_machine_database_moves(
            pokemon, generation, learn_method, form_order, step
        )
    elif learn_method.name == EGG_TYPE:
        return pokemoneggmoveformatter.get_formatted_egg_database_moves(
            pokemon, generation, learn_method, form_order, step
        )
    else:
        raise NotImplementedError(
            f"Cannot process Pokémon move: invalid learn method '{learn_method.name}'"
        )
