from middleware.db.tables import PokemonMoveAvailability
from middleware.exception import InvalidConditionException
from middleware.formatter.dto.machinemove import MachineMove
from middleware.util.helper import generationhelper, machinehelper, languagehelper, pokemonmovehelper, \
    versiongrouphelper, specificcasehelper
from pokedex.db.tables import PokemonMoveMethod, Pokemon, Generation, VersionGroup, PokemonMove
from middleware.db import repository
from collections import OrderedDict
from middleware.connection.conn import session
import re
from pokedex.db import util

"""Format pokemon level moves from database into a pretty format
"""


def get_formatted_machine_database_moves(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod,
                                         form_order: dict, step: int):
    return _get_pokemon_machine_move_forms(pokemon, generation, learn_method, form_order, step)


def _get_preformatteds_database_pokemon_machine_moves(pokemon: Pokemon, generation: Generation, step: int,
                                                      learn_method: PokemonMoveMethod) -> list:
    """
    Get all pokemon machine move for the current step / pokemon and transform them in a list of DTO
    and then filter by the following algo
    Algorithm :
    - if the item is version group specific ( not same item ) , add a toolip next to the name and add it in the list
    - else add it simply in the list
    """
    gen_number = generationhelper.gen_id_to_int(generation.identifier)
    preformatteds = []

    version_groups = pokemonmovehelper.get_pokepedia_version_groups_identifiers_for_pkm_machine_by_step(
        gen_number, step)

    moves = repository.find_moves_by_pokemon_move_method_and_version_groups(
        pokemon, learn_method,
        version_groups
    )

    moves = specificcasehelper.filter_dive_pokemon_move_lgfr(moves)
    for pokemon_move_entity in moves:
        move_name = repository.get_french_move_by_pokemon_move_and_generation(pokemon_move_entity,
                                                                              generation)

        move = _fill_machine_move(move_name['name'], move_name['alias'], pokemon_move_entity,
                                  generationhelper.gen_to_int(
                                      generation))

        preformatteds.append(move)

    return _filter_machine_moves(preformatteds, version_groups, step)


def _filter_machine_moves(preformatteds: list, version_groups: list, step: int) -> list:
    pre_filtered = []
    unspecifics = []
    for preformatted in preformatteds:  # type: MachineMove

        # gen 8 machine moves are in two categories
        if any(version_group == 'sword-shield' for version_group in
               version_groups) and preformatted.is_hm and step == 1:
            continue
        if any(version_group == 'sword-shield' for version_group in
               version_groups) and not preformatted.is_hm and step == 2:
            continue

        different_item = any((machine.name == preformatted.name and machine.item != preformatted.item) for machine in
                             preformatteds)
        different_name = any(machine.item == preformatted.item and machine.name != preformatted.name
                             for machine in
                             preformatteds)
        if different_item:
            vg = preformatted.version_group
            for dto in preformatteds:
                if dto.item == preformatted.item and dto.version_group != preformatted.version_group:
                    preformatted = dto
            preformatted.different_item = True
            preformatted.add_vg_if_possible(vg)
            pre_filtered.append(preformatted)
        elif different_name:
            vg = preformatted.version_group
            for dto in preformatteds:
                if dto.name == preformatted.name and dto.version_group != preformatted.version_group:
                    preformatted = dto
            preformatted.different_name = True
            preformatted.add_vg_if_possible(vg)
            pre_filtered.append(preformatted)
        else:
            if preformatted.name not in unspecifics:
                count = 1
                specific_vgs = [preformatted.version_group]
                for move_dto in preformatteds:
                    if move_dto.item == preformatted.item and move_dto.is_hm == preformatted.is_hm \
                            and move_dto.name == preformatted.name \
                            and move_dto.version_group != preformatted.version_group:
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

    return list(set(pre_filtered))


def _format_machine(move: MachineMove) -> str:
    if move.alias:
        name = f"{move.item[2:]} / " + move.name + "{{!}}" + move.alias
    else:
        name = f"{move.item[2:]} / {move.name}"
    if move.different_name or move.different_item or move.different_version_group:
        name += f" / {versiongrouphelper.get_vg_string_from_vg_identifiers(move.specifics_vgs)}"
    return name


def _sort_pokemon_machine_moves(formatteds: dict) -> list:
    sorted_moves = []

    sorteds_keys = sorted(formatteds, key=lambda k: float(k))
    for key in sorteds_keys:
        sorted_moves.append(formatteds[key])
    return list(dict.fromkeys(sorted_moves))


def _get_formatted_moves_by_pokemons(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod,
                                     step: int):
    """
    Return the fully formatted list of pokemon machine move for a specific pokemon
    """
    pre_formatteds = _get_preformatteds_database_pokemon_machine_moves(pokemon, generation, step, learn_method)
    formatteds = {}

    for move in pre_formatteds:
        string = _format_machine(move)
        weight = _calculate_weight(move)
        if weight in formatteds.keys():
            weight += 0.001
        formatteds[weight] = string

    formatteds = _sort_pokemon_machine_moves(formatteds)
    return formatteds


def _get_pokemon_machine_move_forms(pokemon: Pokemon, generation: Generation, learn_method: PokemonMoveMethod,
                                    form_order: dict, step):
    gen_number = generationhelper.gen_to_int(generation)
    """
    Return a list of  fully formatted pokemon machine move by forms
    """

    if 1 <= gen_number <= 6 or gen_number == 8:
        version_group = repository.find_highest_version_group_by_generation(generation)
    elif gen_number == 7 and step == 1:
        if pokemon.identifier == 'meltan' or pokemon.identifier == 'melmetal':
            version_group = session.query(VersionGroup).filter(
                VersionGroup.identifier == 'lets-go-pikachu-lets-go-eevee').one()
        else:
            version_group = util.get(session, VersionGroup, 'ultra-sun-ultra-moon')
    elif gen_number == 7 and step == 2:
        version_group = util.get(session, VersionGroup, 'lets-go-pikachu-lets-go-eevee')
    else:
        raise InvalidConditionException(f'Invalid generation/step condition : {gen_number} / {step}')

    availability = session.query(PokemonMoveAvailability) \
        .filter(PokemonMoveAvailability.version_group_id == version_group.id) \
        .filter(PokemonMoveAvailability.pokemon_id == pokemon.id) \
        .filter(PokemonMoveAvailability.has_pokepedia_page.is_(True)) \
        .one()

    move_forms = availability.forms

    has_multiple_form_for_move_method = False
    if move_forms:
        has_multiple_form_for_move_method = move_forms[0].machine

    if not move_forms or move_forms[0].has_pokepedia_page or not has_multiple_form_for_move_method:
        if len(form_order) > 1:
            raise RuntimeError(f'Too much form for this pokemon : {pokemon}')
        # noinspection PyUnresolvedReferences
        specy = pokemon.species
        specy_name = specy.name_map[languagehelper.french].replace(' ', '_')  # M. Mime
        form_order_name = next(iter(form_order))
        if specy_name != form_order_name:  # handle case of pokemon with forms on different page like Sylveroy
            specy_name = form_order_name
        return {specy_name: _get_formatted_moves_by_pokemons(pokemon, generation, learn_method, step)}

    custom = move_forms[0].has_pokepedia_page

    if custom:
        # noinspection PyUnresolvedReferences
        specy_name = pokemon.specie.name_map(languagehelper.french)
        return {specy_name: _get_formatted_moves_by_pokemons(pokemon, generation, learn_method, step)}

    if not len(form_order) > 1:
        raise RuntimeError(f'Not enough form for this pokemon : {pokemon}')

    forms = OrderedDict()
    for form_name, form_extra in form_order.items():
        pokemon = repository.find_pokemon_by_french_form_name(pokemon, form_name)
        forms[form_name] = _get_formatted_moves_by_pokemons(pokemon, generation, learn_method, step)

    return forms


# noinspection PyUnresolvedReferences
def _fill_machine_move(name: str, alias: str, pokemon_move_entity: PokemonMove,
                       generation: int) -> MachineMove:
    move = MachineMove()
    move.name = name
    move.alias = alias
    move.is_hm = machinehelper.is_hm(pokemon_move_entity.machine, generation)
    move.item = pokemon_move_entity.machine.item.name_map[languagehelper.french]
    move.version_group = pokemon_move_entity.version_group.identifier
    return move


def _calculate_weight(move: MachineMove):
    """
    Sort by no hm , then hm
    """
    return int(re.search(r'\d+', move.item).group(0)) * (1000 if move.is_hm else 1)
