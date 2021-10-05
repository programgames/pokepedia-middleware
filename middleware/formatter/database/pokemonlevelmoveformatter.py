from middleware.db.tables import PokemonMoveAvailability
from middleware.util.helper import generationhelper, versiongrouphelper, languagehelper
from pokedex.db.tables import PokemonMoveMethod, Pokemon, Generation, VersionGroup, PokemonMove
from middleware.db import repository
from middleware.formatter.dto.levelupmove import LevelUpMove
from collections import OrderedDict
from middleware.connection.conn import session
from pyuca import Collator
import re

"""Format pokemon level moves from database into a pretty format
"""


def get_formatted_level_up_database_moves(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod,
                                          form_order: dict):
    """
     Get pokemon moves from database
    """
    return _get_pokemon_level_move_forms(pokemon, generation, learn_method, form_order)


def _get_preformatteds_database_pokemon_moves(pokemon: Pokemon, generation: Generation,
                                              learn_method: PokemonMoveMethod) -> dict:
    """
    return a dict containing a list of LevelUpMove to ease future formatting/sorting
    """
    gen_number = generationhelper.gen_id_to_int(generation.identifier)
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
        moves = repository.find_moves_by_pokemon_move_method_and_version_group(
            pokemon, learn_method,
            versiongrouphelper.get_version_group_by_gen_and_column(generation, column)
        )
        for pokemon_move_entity in moves:
            french_move = repository.get_french_move_by_pokemon_move_and_generation(pokemon_move_entity,
                                                                                    generation)
            if french_move['name'] in preformatteds:
                move = preformatteds[french_move['name']]
            else:
                move = LevelUpMove()

            move = _fill_leveling_move(move, column, french_move['name'], french_move['alias'], pokemon_move_entity)

            preformatteds[french_move['name']] = move

    return preformatteds


def _format_level(move: LevelUpMove, column: int, previous_weight: int) -> dict:
    """
    Tranform a LevelUpMove object to a dict containing his weight and the pokepedia formatted string
    """
    level = ''
    weight = 0

    if not getattr(move, 'level' + str(column)) and not getattr(move, 'on_evolution' + str(column)) and not getattr(
            move, 'on_start' + str(column)):
        return {
            'level': '-',
            'weight': previous_weight
        }

    if getattr(move, 'on_start' + str(column)):
        level += 'Départ'
        weight = 0

    if getattr(move, 'on_evolution' + str(column)):
        if not level:
            level = 'Évolution'
        else:
            level += ', Évolution'
        weight = 0

    if getattr(move, 'level' + str(column)):
        if getattr(move, 'on_start' + str(column)) or \
                getattr(move, 'on_evolution' + str(column)) \
                or getattr(move, 'level' + str(column) + 'Extra'):
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
        weight = min(int(re.search(r'\d+', getattr(move, 'level' + str(column) + 'Extra')).group()),
                     getattr(move, 'level' + str(column))) if getattr(move,
                                                                      'level' + str(column) + 'Extra') else getattr(
            move, 'level' + str(column))

    return {
        'level': level,
        'weight': max(previous_weight, weight if isinstance(weight, int) else int(re.search(r'\d+', weight).group()))
    }


def _calculate_total_weight(weights: list, formatteds: dict):
    """
    Calculate the position the pokemon level move should have in the list
    """
    total = 0
    for weigh in weights:
        if total == 0 or weigh['weight'] < total:
            total = weigh['weight']

    while True:
        if str(total) in formatteds:
            total += 0.01
        else:
            return str(total)


def _sort_level_moves(formatteds: dict) -> list:
    """
    Sort pokemon level moves , fitst by their weights and then alphabetically
    """
    splitteds = {}
    sorted_moves = []

    sorteds = sorted(formatteds, key=lambda k: float(k))
    pre_sorted = OrderedDict()
    for value in sorteds:
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


def _get_formatted_moves_by_pokemons(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod):
    """
    Return the fully formatted list of pokemon level move for a specific pokemon
    """
    pre_formatteds = _get_preformatteds_database_pokemon_moves(pokemon, generation, learn_method)
    formatteds = {}
    generation = generationhelper.gen_id_to_int(generation.identifier)
    lgpe_vg = session.query(VersionGroup) \
        .filter(VersionGroup.identifier == 'lets-go-pikachu-lets-go-eevee') \
        .one()
    lgpe_availability = repository.get_availability_by_pokemon_and_version_group(pokemon, lgpe_vg)
    if generation == 8:
        for name, move in pre_formatteds.items():
            if move.alias:
                name = name + "{{!}}" + move.alias
            first = _format_level(move, 1, 0)
            total_weight = _calculate_total_weight([first], formatteds)
            formatteds[str(total_weight)] = '{} / {}'.format(name, first['level'])
    elif generation in [1, 2, 5, 6] or (generation == 7 and not lgpe_availability):
        for name, move in pre_formatteds.items():
            if move.alias:
                name = move.alias + "{{!}}" + name
            first = _format_level(move, 1, 0)
            second = _format_level(move, 2, first['weight'])
            total_weight = _calculate_total_weight([first, second], formatteds)
            formatteds[str(total_weight)] = '{} / {} / {}'.format(name, first['level'], second['level'])
    else:
        for name, move in pre_formatteds.items():
            if move.alias:
                name = move.alias + "{{!}}" + name
            first = _format_level(move, 1, 0)
            second = _format_level(move, 2, first['weight'])
            third = _format_level(move, 3, second['weight'])
            total_weight = _calculate_total_weight([first, second, third], formatteds)
            formatteds[total_weight] = '{} / {} / {} / {}'.format(name, first['level'], second['level'], third['level'])

    formatteds = _sort_level_moves(formatteds)
    return formatteds


def _get_pokemon_level_move_forms(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod,
                                  form_order: dict):
    """
    Return a list of  fully formatted pokemon level move by forms
    """
    generation = session.query(Generation).filter(Generation.identifier == generation.identifier).one()

    version_group = repository.find_highest_version_group_by_generation(generation)
    if pokemon.identifier == 'meltan' or pokemon.identifier == 'melmetal':
        version_group = session.query(VersionGroup).filter(
            VersionGroup.identifier == 'lets-go-pikachu-lets-go-eevee').one()
    availability = session.query(PokemonMoveAvailability) \
        .filter(PokemonMoveAvailability.version_group_id == version_group.id) \
        .filter(PokemonMoveAvailability.pokemon_id == pokemon.id) \
        .filter(PokemonMoveAvailability.has_pokepedia_page.is_(True)) \
        .one()

    move_forms = availability.forms

    if not move_forms or move_forms[0].has_pokepedia_page:
        # noinspection PyUnresolvedReferences
        specy = pokemon.species
        specy_name = specy.name_map[languagehelper.french].replace(' ', '_')  # M. Mime
        form_order_name = next(iter(form_order))
        if specy_name != form_order_name:  # handle case of pokemon with forms on different page like Sylveroy
            specy_name = form_order_name
        return {specy_name: _get_formatted_moves_by_pokemons(pokemon, generation, learn_method)}

    custom = move_forms[0].has_pokepedia_page

    if custom:
        # noinspection PyUnresolvedReferences
        specy_name = pokemon.specie.name_map(languagehelper.french)
        return {specy_name: _get_formatted_moves_by_pokemons(pokemon, generation.identifier, learn_method)}

    forms = OrderedDict()
    for form_name, form_extra in form_order.items():
        pokemon = repository.find_pokemon_by_french_form_name(pokemon, form_name)
        forms[form_name] = _get_formatted_moves_by_pokemons(pokemon, generation, learn_method)

    return forms


def _fill_leveling_move(move: LevelUpMove, column: int, name: str, alias:str, pokemon_move_entity: PokemonMove) -> LevelUpMove:
    """
    Update a LevelUpMove
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
        setattr(move, 'level' + str(column) + 'Extra', str(level_extra) + ', ' + str(level))  # Queulorior

    return move
