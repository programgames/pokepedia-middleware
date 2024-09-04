from collections import OrderedDict
import re

from middleware.db import repository
from middleware.exception import InvalidConditionException
from middleware.formatter.database.pokemoneggmoveformatter import _get_formatted_moves_by_pokemons
from middleware.formatter.dto.machinemove import MachineMove
from middleware.models import PokemonMoveAvailability
from middleware.util.helper import pokemonmovehelper, specificcasehelper, versiongrouphelper, machinehelper, \
    generationhelper, languagehelper
from middleware.util.helper.languagehelper import get_pokemon_specy_french_name
from pokeapi.pokemon_v2.models import Pokemon, Generation, MoveLearnMethod, PokemonMove, VersionGroup


# Importe les modèles Django appropriés



def get_formatted_machine_database_moves(pokemon: Pokemon, generation: Generation, learn_method: MoveLearnMethod,
                                         form_order: dict, step: int):
    return _get_pokemon_machine_move_forms(pokemon, generation, learn_method, form_order, step)


def _get_preformatteds_database_pokemon_machine_moves(pokemon: Pokemon, generation: Generation, step: int,
                                                      learn_method: MoveLearnMethod) -> list:
    gen_number = generation.id
    preformatteds = []

    if pokemon.name in ['meltan', 'melmetal'] and gen_number == 7:
        version_groups = ['lets-go-pikachu-lets-go-eevee']
    else:
        version_groups = pokemonmovehelper.get_pokepedia_version_groups_identifiers_for_pkm_machine_by_step(
            gen_number, step)

    if specificcasehelper.is_specific_pokemon_machine_move(pokemon, generation):
        moves = PokemonMove.objects.filter(
            pokemon__identifier__in=['deoxys-normal', 'deoxys-attack', 'deoxys-defense', 'deoxys-speed'],
            pokemon_move_method=learn_method,
            version_group__identifier__in=version_groups
        ).order_by('version_group__identifier')
    else:
        moves = repository.find_moves_by_pokemon_move_method_and_version_groups(
            pokemon, learn_method, version_groups
        )

    moves = specificcasehelper.filter_dive_pokemon_move_lgfr(moves)

    for pokemon_move_entity in moves:
        move_name = repository.get_french_move_by_pokemon_move_and_generation(pokemon_move_entity, generation)

        move = _fill_machine_move(
            move_name['name'], move_name.get('alias'), pokemon_move_entity, generation.id
        )
        preformatteds.append(move)

    return _filter_machine_moves(preformatteds, version_groups, step)


def _filter_machine_moves(preformatteds: list, version_groups: list, step: int) -> list:
    pre_filtered = []
    unspecifics = []

    for preformatted in preformatteds:
        # Filtre des moves de la Gen 8 en fonction du step
        if 'sword-shield' in version_groups:
            if preformatted.is_hm and step == 1:
                continue
            if not preformatted.is_hm and step == 2:
                continue

        different_item = any(
            (machine.name == preformatted.name and machine.item != preformatted.item) for machine in preformatteds
        )
        different_name = any(
            (machine.item == preformatted.item and machine.name != preformatted.name) for machine in preformatteds
        )

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

    return pre_filtered


def _format_machine(move) -> str:
    if move.alias:
        name = f"{move.item[2:]} / {move.alias}"
    else:
        name = f"{move.item[2:]} / {move.name}"

    if move.different_name or move.different_item or move.different_version_group:
        name += f" / {versiongrouphelper.get_vg_string_from_vg_identifiers(move.specifics_vgs)}"
    return name


def _sort_pokemon_machine_moves(formatteds: dict) -> list:
    # noinspection DuplicatedCode
    splitteds = {}
    sorted_moves = []

    sorteds = sorted(formatteds, key=lambda k: float(k))
    pre_sorted = OrderedDict((value, formatteds[value]) for value in sorteds)

    for level, formatted in pre_sorted.items():
        level = float(level)
        splitteds.setdefault(int(level), {})[level] = formatted

    for key, splitteds_moves in splitteds.items():
        splitteds[key] = sorted(splitteds_moves.values(), key=lambda move: move.name)

    last = None
    for moves in splitteds.values():
        for move in moves:
            if move != last:
                last = move
                sorted_moves.append(move)
    return sorted_moves


def _get_pokemon_machine_move_forms(pokemon: Pokemon, generation: Generation, learn_method: MoveLearnMethod,
                                    form_order: dict, step):
    gen_number = generationhelper.gen_to_int(generation)

    if 1 <= gen_number <= 6:
        version_group = repository.find_highest_version_group_by_generation(generation)
    elif gen_number == 7 and step == 1:
        version_group = VersionGroup.objects.get(name='ultra-sun-ultra-moon')
    elif gen_number == 7 and step == 2 or gen_number == 8 and step == 2:
        version_group = VersionGroup.objects.get(name='lets-go-pikachu-lets-go-eevee')
    else:
        raise InvalidConditionException(f'Invalid generation/step condition: {gen_number} / {step}')

    availability = PokemonMoveAvailability.objects.filter(
        version_group=version_group, pokemon=pokemon, has_pokepedia_page=True
    ).first()

    if not availability or not availability.forms:
        specy_name = get_pokemon_specy_french_name(pokemon.pokemon_species).replace(' ', '_')
        form_order_name = next(iter(form_order))
        if specy_name != form_order_name:
            specy_name = form_order_name
        return {specy_name: _get_formatted_moves_by_pokemons(pokemon, generation, learn_method, step)}

    if availability.forms[0].has_pokepedia_page:
        specy_name = get_pokemon_specy_french_name(pokemon.pokemon_species)

        return {specy_name: _get_formatted_moves_by_pokemons(pokemon, generation, learn_method, step)}

    forms = OrderedDict()
    for form_name, form_extra in form_order.items():
        pokemon = repository.find_pokemon_by_french_form_name(pokemon, form_name)
        forms[form_name] = _get_formatted_moves_by_pokemons(pokemon, generation, learn_method, step)

    return forms


def _fill_machine_move(name: str, alias: str, pokemon_move_entity: PokemonMove, generation: int):
    move = MachineMove()
    move.name = name
    move.alias = alias
    move.is_hm = machinehelper.is_hm(pokemon_move_entity.machine, generation)
    move.item = languagehelper.get_item_french_name(pokemon_move_entity.machine.item)
    move.version_group = pokemon_move_entity.version_group.name
    return move


def _calculate_weight(move):
    return int(re.search(r'\d+', move.item).group(0)) * (1000 if move.is_hm else 1)
