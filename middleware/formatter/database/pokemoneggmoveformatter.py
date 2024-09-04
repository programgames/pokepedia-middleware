from random import random
from collections import OrderedDict

from pyuca import Collator

from middleware.exception import InvalidConditionException
from middleware.formatter.dto.eggmove import EggMove
from middleware.models import PokemonMoveAvailability
from middleware.util.helper import (
    generationhelper, pokemonmovehelper, versiongrouphelper, specificcasehelper
)
from middleware.db import repository
from middleware.util.helper.languagehelper import get_pokemon_specy_french_name
from pokeapi.pokemon_v2.models import Pokemon, Generation, VersionGroup, Move, MoveLearnMethod

"""Format pokemon egg moves from database into a pretty format"""


def get_formatted_egg_database_moves(pokemon: Pokemon, generation: Generation, learn_method: MoveLearnMethod,
                                     form_order: dict, step: int):
    return _get_pokemon_egg_move_forms(pokemon, generation, learn_method, form_order, step)


def _get_preformatteds_database_pokemon_egg_moves(pokemon: Pokemon, generation: Generation, step: int,
                                                  learn_method: MoveLearnMethod) -> list:
    gen_number = generationhelper.gen_name_to_gen_number(generation.name)
    preformatteds = []

    version_groups = _get_version_groups_for_pokemon(pokemon, gen_number, step)

    original_pokemon = pokemon
    pokemon = repository.find_minimal_pokemon_in_evolution_chain(pokemon, generation)
    moves = repository.find_moves_by_pokemon_move_method_and_version_groups_with_concat(
        pokemon, learn_method, version_groups
    )

    moves = specificcasehelper.remove_dive_move_lgfr(moves)
    moves = specificcasehelper.remove_egg_move_exceptions(generation, pokemon, moves)

    for move_with_vg in moves:
        move_name = repository.get_french_move_name_by_move_and_generation(move_with_vg.Move, generation)

        move_dto = _fill_egg_move(
            original_pokemon, learn_method, move_name['name'], move_name['alias'],
            move_with_vg, generationhelper.gen_to_int(generation), move_with_vg.Move, step
        )
        preformatteds.append(move_dto)

    return preformatteds


def _get_version_groups_for_pokemon(pokemon, gen_number, step):
    if (pokemon.name == 'meltan' or pokemon.name == 'melmetal') and gen_number == 7:
        return ['lets-go-pikachu-lets-go-eevee']
    return pokemonmovehelper.get_pokepedia_version_groups_identifiers_for_pkm_egg_by_step(gen_number, step)


def _filter_egg_moves(preformatteds: list, version_groups: list, step: int) -> list:
    pre_filtered = []
    unspecifics = []

    for preformatted in preformatteds:  # type: EggMove
        if preformatted.name not in unspecifics:
            count = 1
            specific_vgs = [preformatted.version_group]
            for move_dto in preformatteds:
                if move_dto.name == preformatted.name and move_dto.version_group != preformatted.version_group:
                    count += 1
                    if move_dto.version_group not in specific_vgs:
                        specific_vgs.append(move_dto.version_group)
            if count < len(version_groups):
                preformatted.specifics_vgs = specific_vgs
                preformatted.different_version_group = True
                pre_filtered.append(preformatted)
            else:
                unspecifics.append(preformatted.name)
                pre_filtered.append(preformatted)

    return pre_filtered


def _get_pokemon_eggmoove_name(parent: dict, gen: Generation, step: int):
    pokemon = parent['pokemon']
    vgs = parent['version_groups']

    pkmname = get_pokemon_specy_french_name(pokemon.pokemon_species).replace(' ', '_')  # M.mime
    if pokemon.forms[0].form_identifier == 'alola':
        pkmname += 'forme(Alola)'
    if pokemon.forms[0].form_identifier == 'galar':
        pkmname += 'forme(Galar)'

    genvgs = repository.find_version_group_identifier_by_generation(gen, step)
    if len(vgs) != len(genvgs):
        pkmname += f" jeu({versiongrouphelper.get_vg_string_from_vg_identifiers([vg.identifier for vg in vgs])})"

    pkmname += ', '
    return pkmname


def _format_egg_move(move: EggMove, gen: Generation, step: int) -> str:
    name = move.name
    if move.specifics_vgs:
        name += f" jeu({versiongrouphelper.get_vg_string_from_vg_identifiers(move.specifics_vgs)})"

    name += ' / '
    name += _format_parents(move.parents['level-up'], gen, step)
    name += ' / '
    name += _format_parents(move.parents['egg'], gen, step)

    return name


def _format_parents(parents, gen: Generation, step: int) -> str:
    names = []
    for order, parent_set in parents.items():
        for pokemon in parent_set.values():
            names.append(_get_pokemon_eggmoove_name(pokemon, gen, step))
    return ', '.join(names)


def _sort_pokemon_egg_moves(formatteds: dict) -> list:
    sorted_moves = []
    sorteds = sorted(formatteds.items(), key=lambda k: k[0])

    splitteds = {}
    for weight, formatted in sorteds:
        level = int(float(weight))
        splitteds.setdefault(level, []).append(formatted)

    collator = Collator()
    for level, moves in sorted(splitteds.items()):
        sorted_moves.extend(sorted(moves, key=collator.sort_key))

    return sorted_moves


def _get_formatted_moves_by_pokemons(pokemon: Pokemon, generation: Generation, learn_method: MoveLearnMethod,
                                     step: int):
    """
    Return the fully formatted list of Pokémon machine move for a specific Pokémon
    """
    pre_formatteds = _get_preformatteds_database_pokemon_egg_moves(pokemon, generation, step, learn_method)
    formatteds = {}

    for move in pre_formatteds:
        string = _format_egg_move(move, generation, step)
        weight = _calculate_weight(move)
        while weight in formatteds:
            weight += random()
        formatteds[weight] = string

    return _sort_pokemon_egg_moves(formatteds)


def _get_pokemon_egg_move_forms(pokemon: Pokemon, generation: Generation, learn_method: MoveLearnMethod,
                                form_order: dict, step):
    gen_number = generationhelper.gen_to_int(generation)

    if gen_number in {1, 2, 3, 4, 5, 6, 8}:
        version_group = repository.find_highest_version_group_by_generation(generation)
    elif gen_number == 7:
        version_group = _get_version_group_for_gen7(pokemon, step)
    else:
        raise InvalidConditionException(f'Invalid generation/step condition: {gen_number} / {step}')

    availability = PokemonMoveAvailability.objects.filter(
        version_group=version_group,
        pokemon=pokemon,
        has_pokepedia_page=True
    ).first()

    if not availability or not availability.forms or not availability.forms[0].egg:
        if len(form_order) > 1:
            raise RuntimeError(f'Too many forms for this pokemon: {pokemon}')
        specy_name = get_pokemon_specy_french_name(pokemon.pokemon_species).replace(' ', '_')
        form_order_name = next(iter(form_order))
        if specy_name != form_order_name:  # handle case of Pokémon with forms on different page like Sylveroy
            specy_name = form_order_name
        return {specy_name: _get_formatted_moves_by_pokemons(pokemon, generation, learn_method, step)}

    if availability.forms[0].has_pokepedia_page:
        specy_name = get_pokemon_specy_french_name(pokemon.pokemon_species).replace(' ', '_')
        return {specy_name: _get_formatted_moves_by_pokemons(pokemon, generation, learn_method, step)}

    if not form_order:
        raise RuntimeError(f'Not enough forms for this pokemon: {pokemon}')

    forms = OrderedDict()
    for form_name in form_order:
        form_pokemon = repository.find_pokemon_by_french_form_name(pokemon, form_name)
        forms[form_name] = _get_formatted_moves_by_pokemons(form_pokemon, generation, learn_method, step)

    return forms


def _get_version_group_for_gen7(pokemon, step):
    if step == 1 and pokemon.name not in ['meltan', 'melmetal']:
        return VersionGroup.objects.get(identifier='ultra-sun-ultra-moon')
    return VersionGroup.objects.get(identifier='lets-go-pikachu-lets-go-eevee')


def _fill_egg_move(pokemon: Pokemon, learn_method: MoveLearnMethod, name: str, alias: str, move_with_vg,
                   generation: int, eggmove: Move, step: int) -> EggMove:
    move = EggMove()
    move.name = alias or name
    move.alias = alias
    move.move = eggmove
    move.version_groups = move_with_vg[1].split('/')

    vgs = repository.find_version_group_identifier_by_generation(generation, step)
    if len(move.version_groups) != len(vgs):
        for vg in move.version_groups:
            move.add_vg_if_possible(vg)

    _fill_parents(pokemon, move, generation, step)
    return move

def _calculate_weight(move: EggMove) -> float:
    """
    Calculate a weight for sorting moves by name.
    """
    weight = 0
    divisor = 10
    for char in move.name:
        weight += (ord(char) / divisor) / 100
        divisor *= 10
    return weight

def _fill_parents(pokemon: Pokemon, move: EggMove, gen: int, step: int):
    """
    Fill the parent Pokémon information for the given move.
    """
    move.parents = repository.find_pokemon_learning_move_by_egg_groups(pokemon, move.move, gen, step)