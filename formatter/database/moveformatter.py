from pokedex.db.tables import PokemonMoveMethod, Pokemon, Generation, VersionGroup

from db import repository, PokemonMoveAvailability
from formatter.dto.levelupmove import LevelUpMove
from formatter.pokemonmovefiller import fill_leveling_move
from util.helper import languagehelper
from util.helper.generationhelper import get_version_group_by_gen_and_column
from collections import OrderedDict
from operator import itemgetter
from connection.conn import session

def get_formatted_level_up_database_moves(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod):
    return get_move_forms(pokemon, generation, learn_method)


def _get_preformatteds_database_pokemon_moves(pokemon: Pokemon, generation: int, learn_method: PokemonMoveMethod):
    preformatteds = {}
    if generation in [3, 4, 7]:
        columns = 3
    elif generation in [1, 2, 5, 6]:
        columns = 2
    else:
        columns = 1

    for column in range(1, columns):
        moves = repository.find_moves_by_pokemon_move_method_and_version_group(pokemon, learn_method,
                                                                               get_version_group_by_gen_and_column(
                                                                                   generation, column))
        for pokemon_move_entity in moves:
            pass
            french_move_name = repository.find_french_move_by_pokemon_move_and_generation(pokemon_move_entity,
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
            'level': '—',
            'weight': previous_weight
        }

    if getattr(move, 'onStart' + str(column)):
        level += 'Départ'
        weight = 0

    if getattr(move, 'onEvolution' + str(column)):
        level += 'Départ'
        weight = 0

    if getattr(move, 'level' + str(column)):
        if getattr(move, 'onStart' + str(column)) or getattr(move, 'onEvolution' + str(column)) or getattr(move,
                                                                                                           'level' + str(
                                                                                                               column) + 'Extra'):
            if not level:
                level += 'N.' + getattr(move, 'level' + str(column))
                weight = getattr(move, 'level' + str(column))
            else:
                level += ', N.' + getattr(move, 'level' + str(column))
                weight = getattr(move, 'level' + str(column))
        else:
            level += getattr(move, 'level' + str(column))
            weight = getattr(move, 'level' + str(column))

    if getattr(move, 'level' + str(column) + 'Extra'):
        level += ', N.' + getattr(move, 'level' + str(level) + 'Extra')
        weight = getattr(move, 'level' + str(column) + 'Extra') if getattr(move,
                                                                           level + str(column) + 'Extra') else getattr(
            move, 'level' + str(column))

    return {
        'level': level,
        'weight': max(previous_weight, weight)
    }


def _calculate_total_weight(weights: list, formatteds: dict):
    total = 0
    for weigh in weights:
        if total == 0 or weigh['weight'] < total:
            total = weigh['weight']

    while True:
        if str(total) in formatteds:
            total += 0.1
        else:
            return str(total)


def _sort_level_moves(formatteds: dict):
    preformatteds = sorted(formatteds)
    splitteds = {}
    sorted = []

    for level, formatted in preformatteds:
        if int(level) not in splitteds:
            splitteds[int(level)] = []
        splitteds[int(level)][level] = formatted

    for key, splitteds_moves in splitteds:
        # TODO test
        splitteds[key] = OrderedDict(sorted(splitteds_moves.items(), key=itemgetter(1)))

    for splitted in splitteds:
        for level, move in splitted:
            sorted.append(move)

    return sorted


def _formated_by_pokemon(pokemon: Pokemon, generation: int, learn_method: PokemonMoveMethod):
    pre_formatteds = _get_preformatteds_database_pokemon_moves(pokemon, generation, learn_method)
    formatteds = {}
    if generation == 8:
        for name, move in pre_formatteds:
            first = _format_level(move, 1, 0)
            total_weight = _calculate_total_weight([first], formatteds)
            formatteds[str(total_weight)] = '{} / {}'.format(name, first['level'])
    elif generation in [1, 2, 5, 6]:
        for name, move in pre_formatteds:
            first = _format_level(move, 1, 0)
            second = _format_level(move, 2, first['weight'])
            total_weight = _calculate_total_weight([first, second], formatteds)
            formatteds[str(total_weight)] = '{} / {} / {}'.format(name, first['level'], second['level'])
    else:
        for name, move in pre_formatteds:
            first = _format_level(move, 1, 0)
            second = _format_level(move, 2, first['weight'])
            third = _format_level(move, 3, second['weight'])
            total_weight = _calculate_total_weight([first, second, third], formatteds)
            formatteds[total_weight] = '{} / {} / {} / {}'.format(name, first['level'], second['level'], third['level'])

    formatteds = _sort_level_moves(formatteds)
    return formatteds


def get_move_forms(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod):
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
        specy =  pokemon.species
        specy_name = specy.name_map[languagehelper.french]

        return {specy_name: _formated_by_pokemon(pokemon, generation.identifier, learn_method)}

    custom = list(move_forms.values())[0].has_custom_pokepedia_page()

    if custom:
        specy_name = pokemon.specie.name_map('fr')
        return {specy_name: _formated_by_pokemon(pokemon, generation.identifier, learn_method)}

    forms = {}
    for move_form in move_forms:
        availability = session.query(PokemonMoveAvailability).filter(
            PokemonMoveAvailability.version_group == version_group, PokemonMoveAvailability.pokemon == pokemon,
            PokemonMoveAvailability.has_pokepedia_page.is_(False))

        forms['test'] = 2
