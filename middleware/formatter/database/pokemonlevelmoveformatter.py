from collections import OrderedDict
from pyuca import Collator
import re

from middleware.models import PokemonMoveAvailability
from middleware.util.helper import generationhelper, versiongrouphelper
from middleware.db import repository
from middleware.formatter.dto.levelupmove import LevelUpMove
from middleware.util.helper.languagehelper import get_pokemon_specy_french_name
from pokeapi.pokemon_v2.models import Pokemon, Generation, VersionGroup, PokemonMove, MoveLearnMethod

"""Format Pokemon level moves from database into a pretty format"""


def get_formatted_level_up_database_moves(pokemon: Pokemon, generation: Generation, learn_method: MoveLearnMethod,
                                          form_order: dict):
    """
    Get Pokémon moves from the database and format them.
    """
    return _get_pokemon_level_move_forms(pokemon, generation, learn_method, form_order)


def _get_preformatteds_database_pokemon_moves(pokemon: Pokemon, generation: Generation,
                                              learn_method: MoveLearnMethod) -> dict:
    """
    Return a dict containing a list of LevelUpMove to ease future formatting/sorting.
    """
    gen_number = generationhelper.gen_name_to_gen_number(generation.name)
    preformatteds = {}
    columns = _determine_columns(gen_number, pokemon)

    for column in range(1, columns + 1):
        version_group = versiongrouphelper.get_version_group_by_gen_and_column(generation, column)
        moves = repository.find_moves_by_pokemon_move_method_and_version_group(pokemon, learn_method, version_group)

        for pokemon_move_entity in moves:
            french_move = repository.get_french_move_by_pokemon_move_and_generation(pokemon_move_entity, generation)
            move = preformatteds.get(french_move['name'], LevelUpMove())
            move = _fill_leveling_move(move, column, french_move['name'], french_move['alias'], pokemon_move_entity)
            preformatteds[french_move['name']] = move

    return preformatteds


def _determine_columns(gen_number: int, pokemon: Pokemon) -> int:
    """
    Determine the number of columns based on the generation and Pokémon availability.
    """
    if gen_number == 7:
        lgpe = VersionGroup.objects.get(name='lets-go-pikachu-lets-go-eevee')
        availability = repository.get_availability_by_pokemon_and_version_group(pokemon, lgpe)
        return 3 if availability else 2
    elif gen_number in {3, 4}:
        return 3
    elif gen_number in {1, 2, 5, 6}:
        return 2
    else:
        return 1


def _format_level(move: LevelUpMove, column: int, previous_weight: int) -> dict:
    """
    Transform a LevelUpMove object to a dict containing its weight and the formatted string.
    """
    level = ''
    weight = 0

    if not any(getattr(move, attr + str(column)) for attr in ['level', 'on_evolution', 'on_start']):
        return {'level': '-', 'weight': previous_weight}

    if getattr(move, 'on_start' + str(column)):
        level = 'Départ'
        weight = 0

    if getattr(move, 'on_evolution' + str(column)):
        level = level + ', ' if level else ''
        level += 'Évolution'
        weight = 0

    if getattr(move, 'level' + str(column)):
        level_str = str(getattr(move, 'level' + str(column)))
        #TODO a corriger levelExtra
        if any(getattr(move, attr + str(column), None) for attr in ['on_start', 'on_evolution', 'levelExtra']):
            level = level + ', N.' + level_str if level else 'N.' + level_str
        else:
            level = level_str
        weight = getattr(move, 'level' + str(column))

    if getattr(move, 'level' + str(column) + 'Extra'):
        extra_level = str(getattr(move, 'level' + str(column) + 'Extra'))
        level += ', N.' + extra_level
        weight = min(int(re.search(r'\d+', extra_level).group()), weight) if extra_level else weight

    return {'level': level, 'weight': max(previous_weight, weight)}


def _calculate_total_weight(weights: list, formatteds: dict) -> str:
    """
    Calculate the position the Pokémon level move should have in the list.
    """
    total = min(weight['weight'] for weight in weights if
                weight is not None and weight['weight'] is not None and weight['level'] != '-')

    while True:
        if str(total) in formatteds:
            total += 0.01
        else:
            return str(total)


# noinspection DuplicatedCode
def _sort_level_moves(formatteds: dict) -> list:
    """
    Sort Pokémon level moves, first by their weights and then alphabetically.
    """
    splitteds = {}
    sorted_moves = []

    sorteds = sorted(formatteds, key=lambda k: float(k))
    pre_sorted = OrderedDict((k, formatteds[k]) for k in sorteds)

    for level, formatted in pre_sorted.items():
        level = float(level)
        splitteds.setdefault(int(level), {})[level] = formatted

    collator = Collator()
    for key, moves in splitteds.items():
        sorted_moves.extend(sorted(moves.values(), key=collator.sort_key))

    return sorted_moves


def _get_formatted_moves_by_pokemons(pokemon: Pokemon, generation: Generation, learn_method: MoveLearnMethod):
    """
    Return the fully formatted list of Pokémon level move for a specific Pokémon.
    """
    pre_formatteds = _get_preformatteds_database_pokemon_moves(pokemon, generation, learn_method)
    formatteds = {}
    generation_number = generationhelper.gen_name_to_gen_number(generation.name)

    for name, move in pre_formatteds.items():
        name = move.alias  if move.alias else name.name

        first_weight = _format_level(move, 1, 0)

        # On crée la liste de weights en utilisant d'abord le premier poids
        weights = [
            first_weight,
            _format_level(move, 2, first_weight['weight']),
            _format_level(move, 3, _format_level(move, 2, first_weight['weight'])['weight']) if generation_number in {3,
                                                                                                                      4,
                                                                                                                      7} else None
        ]

        total_weight = _calculate_total_weight(weights, formatteds)
        formatteds[total_weight] = ' / '.join([name] + [w['level'] for w in weights if w])

    return _sort_level_moves(formatteds)


def _get_pokemon_level_move_forms(pokemon: Pokemon, generation: Generation, learn_method: MoveLearnMethod,
                                  form_order: dict):
    """
    Return a list of fully formatted Pokémon level move by forms.
    """
    generation = Generation.objects.get(name=generation.name)
    version_group = repository.find_highest_version_group_by_generation(generation)

    if pokemon.name in {'meltan', 'melmetal'}:
        version_group = VersionGroup.objects.get(name='lets-go-pikachu-lets-go-eevee')

    availability = PokemonMoveAvailability.objects.filter(
        version_group=version_group, pokemon=pokemon, has_pokepedia_page=True
    ).first()

    if not availability or not availability.forms or not availability.forms.all().first() or not availability.forms.all().first().has_pokepedia_page:
        if len(form_order) > 1:
            raise RuntimeError(f'Too many forms for this Pokemon: {pokemon}')

        specy_name = get_pokemon_specy_french_name(pokemon.pokemon_species).name.replace(' ', '_')
        form_order_name = next(iter(form_order))

        if specy_name != form_order_name:  # handle case of Pokémon with forms on different pages like Sylveroy
            specy_name = form_order_name

        return {specy_name: _get_formatted_moves_by_pokemons(pokemon, generation, learn_method)}

    if availability.forms[0].has_pokepedia_page:
        specy_name = get_pokemon_specy_french_name(pokemon.pokemon_species).replace(' ', '_')
        return {specy_name: _get_formatted_moves_by_pokemons(pokemon, generation, learn_method)}

    if not form_order:
        raise RuntimeError(f'Not enough forms for this Pokemon: {pokemon}')

    forms = OrderedDict()
    for form_name in form_order:
        form_pokemon = repository.find_pokemon_by_french_form_name(pokemon, form_name)
        forms[form_name] = _get_formatted_moves_by_pokemons(form_pokemon, generation, learn_method)

    return forms


def _fill_leveling_move(move: LevelUpMove, column: int, name: str, alias: str,
                        pokemon_move_entity: PokemonMove) -> LevelUpMove:
    """
    Update a LevelUpMove with level information.
    """
    move.name = name
    move.alias = alias
    level = pokemon_move_entity.level

    if level == 1:
        setattr(move, 'on_start' + str(column), True)
    elif level == 0:
        setattr(move, 'on_evolution' + str(column), True)
    elif getattr(move, 'level' + str(column)) is None:
        setattr(move, 'level' + str(column), level)
    elif getattr(move, 'level' + str(column) + 'Extra') is None:
        setattr(move, 'level' + str(column) + 'Extra', str(level))
    else:
        level_extra = getattr(move, 'level' + str(column) + 'Extra')
        setattr(move, 'level' + str(column) + 'Extra', f"{level_extra}, {level}")

    return move
