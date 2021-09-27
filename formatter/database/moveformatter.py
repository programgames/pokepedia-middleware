from pokedex.db.tables import PokemonMoveMethod, Pokemon, Generation, PokemonForm, VersionGroup
from db import repository, PokemonMoveAvailability
from formatter.dto.levelupmove import LevelUpMove
from formatter.pokemonmovefiller import fill_leveling_move
from util.helper import languagehelper, generationhelper
from util.helper.generationhelper import get_version_group_by_gen_and_column
from collections import OrderedDict
from connection.conn import session
from pyuca import Collator
import re


def get_formatted_level_up_database_moves(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod,
                                          form_order: list):
    return get_move_forms(pokemon, generation, learn_method, form_order)


def _get_preformatteds_database_pokemon_moves(pokemon: Pokemon, generation: Generation,
                                              learn_method: PokemonMoveMethod):
    gen_number = generationhelper.get_gen_number_by_identifier(generation.identifier)
    preformatteds = {}
    if gen_number == 7:
        lgpe = session.query(VersionGroup) \
            .filter(VersionGroup.identifier == 'lets-go-pikachu-lets-go-eevee') \
            .one()
        availability = repository.get_availability_by_pokemon_and_version_group(pokemon, lgpe)
        if availability:
            columns = 3
        else:
            columns = 2
    elif gen_number in [3, 4]:
        columns = 3
    elif gen_number in [1, 2, 5, 6]:
        columns = 2
    else:
        columns = 1

    for column in range(1, columns + 1):
        moves = repository.find_moves_by_pokemon_move_method_and_version_group(pokemon, learn_method,
                                                                               get_version_group_by_gen_and_column(
                                                                                   generation, column))
        for pokemon_move_entity in moves:
            french_move_name = repository.get_french_move_by_pokemon_move_and_generation(pokemon_move_entity,
                                                                                         generation)
            if french_move_name in preformatteds:
                move = preformatteds[french_move_name]
            else:
                move = LevelUpMove()

            move = fill_leveling_move(move, column, french_move_name, pokemon_move_entity)

            preformatteds[french_move_name] = move

    return preformatteds


def _format_level(move: LevelUpMove, column: int, previous_weight: int) -> dict:
    level = ''
    weight = 0

    if not getattr(move, 'level' + str(column)) and not getattr(move, 'onEvolution' + str(column)) and not getattr(
            move, 'onStart' + str(column)):
        return {
            'level': '-',
            'weight': previous_weight
        }

    if getattr(move, 'onStart' + str(column)):
        level += 'Départ'
        weight = 0

    if getattr(move, 'onEvolution' + str(column)):
        if not level:
            level = 'Évolution'
        else:
            level += ', Évolution'
        weight = 0

    if getattr(move, 'level' + str(column)):
        if getattr(move, 'onStart' + str(column)) or getattr(move, 'onEvolution' + str(column)) or getattr(move,
                                                                                                           'level' + str(
                                                                                                               column) + 'Extra'):
            if not level:
                level += 'N.' + str(getattr(move, 'level' + str(column)))
                weight = getattr(move, 'level' + str(column))
            else:
                level += ', N.' + str(getattr(move, 'level' + str(column)))
                weight = getattr(move, 'level' + str(column))
        else:
            level += str(getattr(move, 'level' + str(column)))
            weight = getattr(move, 'level' + str(column))

    if getattr(move, 'level' + str(column) + 'Extra'):
        level += ', N.' + str(getattr(move, 'level' + str(column) + 'Extra'))
        weight = getattr(move, 'level' + str(column) + 'Extra') if getattr(move, 'level' + str(
            column) + 'Extra') else getattr(move, 'level' + str(column))

    return {
        'level': level,
        'weight': max(previous_weight, weight if isinstance(weight, int) else int(re.search(r'\d+', weight).group()))
    }


def _calculate_total_weight(weights: list, formatteds: dict):
    total = 0
    for weigh in weights:
        if total == 0 or weigh['weight'] < total:
            total = weigh['weight']

    while True:
        if str(total) in formatteds:
            total += 0.01
        else:
            return str(total)


def _sort_level_moves(formatteds: dict):
    splitteds = {}
    sorted_moves = []

    sortedss = sorted(formatteds, key=lambda k: float(k))
    pre_sorted = OrderedDict()
    for value in sortedss:
        pre_sorted[value] = formatteds[value]
    for level, formatted in pre_sorted.items():
        level = float(level)

        if int(level) not in splitteds:
            splitteds[int(level)] = {}
        splitteds[int(level)][level] = formatted

    for key, splitteds_moves in splitteds.items():
        c = Collator()

        splitteds[key] = sorted(splitteds_moves.values(), key=c.sort_key)

    for level, moves in splitteds.items():
        for move in moves:
            sorted_moves.append(move)

    return sorted_moves


def _formated_by_pokemon(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod):
    pre_formatteds = _get_preformatteds_database_pokemon_moves(pokemon, generation, learn_method)
    formatteds = {}
    generation = generationhelper.get_gen_number_by_identifier(generation.identifier)
    lgpe_vg = session.query(VersionGroup) \
        .filter(VersionGroup.identifier == 'lets-go-pikachu-lets-go-eevee') \
        .one()
    lgpe_availability = repository.get_availability_by_pokemon_and_version_group(pokemon, lgpe_vg)
    if generation == 8:
        for name, move in pre_formatteds.items():
            first = _format_level(move, 1, 0)
            total_weight = _calculate_total_weight([first], formatteds)
            formatteds[str(total_weight)] = '{} / {}'.format(name, first['level'])
    elif generation in [1, 2, 5, 6] or (generation == 7 and not lgpe_availability):
        for name, move in pre_formatteds.items():
            first = _format_level(move, 1, 0)
            second = _format_level(move, 2, first['weight'])
            total_weight = _calculate_total_weight([first, second], formatteds)
            formatteds[str(total_weight)] = '{} / {} / {}'.format(name, first['level'], second['level'])
    else:
        for name, move in pre_formatteds.items():
            first = _format_level(move, 1, 0)
            second = _format_level(move, 2, first['weight'])
            third = _format_level(move, 3, second['weight'])
            total_weight = _calculate_total_weight([first, second, third], formatteds)
            formatteds[total_weight] = '{} / {} / {} / {}'.format(name, first['level'], second['level'], third['level'])

    formatteds = _sort_level_moves(formatteds)
    return formatteds


def get_move_forms(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod, form_order: list):
    generation = session.query(Generation).filter(Generation.identifier == generation.identifier).one()

    version_group = repository.find_highest_version_group_by_generation(generation)

    availability = session.query(PokemonMoveAvailability) \
        .filter(PokemonMoveAvailability.version_group_id == version_group.id) \
        .filter(PokemonMoveAvailability.pokemon_id == pokemon.id) \
        .filter(PokemonMoveAvailability.is_default.is_(True)) \
        .filter(PokemonMoveAvailability.has_pokepedia_page.is_(True)) \
        .one()

    move_forms = availability.forms

    if not move_forms:
        specy = pokemon.species
        specy_name = specy.name_map[languagehelper.french].replace(' ', '_')  # M. Mime

        return {specy_name: _formated_by_pokemon(pokemon, generation, learn_method)}

    custom = move_forms[0].has_pokepedia_page

    if custom:
        specy_name = pokemon.specie.name_map(languagehelper.french)
        return {specy_name: _formated_by_pokemon(pokemon, generation.identifier, learn_method)}

    forms = OrderedDict()
    for form_name in form_order:
        pokemon = repository.find_pokemon_by_french_form_name(pokemon, form_name)
        forms[form_name] = _formated_by_pokemon(pokemon, generation, learn_method)

    return forms
