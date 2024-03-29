from middleware.connection import sqlite
from pokedex.db.tables import *

from middleware.db.tables import PokemonMoveAvailability, MoveNameChangelog
from middleware.connection.conn import session
from middleware.db.tables import PokemonTypePast, CacheItem
from middleware.util.helper import languagehelper, generationhelper, specificcasehelper
import functools
from collections import OrderedDict

"""
Contains functions using the repository pattern to encapsulate database requests
"""


def get_default_gen8_national_dex_pokemon_number():
    return [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
        42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 72, 73, 77, 78, 79, 80,
        81, 82, 83, 90, 91, 92, 93, 94, 95, 98, 99, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114,
        115, 116, 117, 118,
        119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139,
        140, 141,
        142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 163, 164, 169, 170, 171, 172, 173, 174, 175, 176, 177,
        178, 182,
        183, 184, 185, 186, 194, 195, 196, 197, 199, 202, 206, 208, 211, 212, 213, 214, 215, 220, 221, 222, 223,
        224, 225,
        226, 227, 230, 233, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252,
        253, 254,
        255, 256, 257, 258, 259, 260, 263, 264, 270, 271, 272, 273, 274, 275, 278, 279, 280, 281, 282, 290, 291,
        292, 293,
        294, 295, 298, 302, 303, 304, 305, 306, 309, 310, 315, 318, 319, 320, 321, 324, 328, 329, 330, 333, 334,
        337, 338,
        339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 355, 356, 359, 360, 361, 362, 363, 364, 365,
        369, 371,
        372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 403, 404, 405, 406, 407, 415, 416,
        420, 421,
        422, 423, 425, 426, 427, 428, 434, 435, 436, 437, 438, 439, 440, 442, 443, 444, 445, 446, 447, 448, 449,
        450, 451, 452, 453, 454, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 470, 471, 473, 474, 475,
        477, 478, 479, 480,
        481, 482, 483, 484, 485, 486, 487, 488, 494, 506, 507, 508, 509, 510, 517, 518, 519, 520, 521, 524, 525,
        526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 543, 544, 545, 546, 547, 548, 549,
        550, 551,
        552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572,
        573, 574,
        575, 576, 577, 578, 579, 582, 583, 584, 587, 588, 589, 590, 591, 592, 593, 595, 596, 597, 598, 599, 600,
        601, 605,
        606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626,
        627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647,
        649, 659, 660, 661, 662, 663,
        674, 675, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695,
        696, 697,
        698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718,
        719, 721,
        722, 723, 724, 725, 726, 727, 728, 729, 730, 736, 737, 738, 742, 743, 744, 745, 746, 747, 748, 749, 750,
        751, 752,
        753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773,
        776, 777,
        778, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799,
        800, 801,
        802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822,
        823, 824,
        825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845,
        846, 847,
        848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868,
        869, 870,
        871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891,
        892, 893, 894, 895, 896, 897, 898
    ]


# noinspection PyUnresolvedReferences
def find_default_pokemons_in_national_dex(start: int, end: int):
    national_pokedex = session.query(Pokedex).filter(Pokedex.identifier == 'national').one()

    id_results = session.query(PokemonSpecies.id) \
        .select_from(PokemonDexNumber) \
        .join(PokemonDexNumber.species) \
        .filter(PokemonDexNumber.pokedex_id == national_pokedex.id) \
        .filter(PokemonDexNumber.pokedex_number >= start) \
        .filter(PokemonDexNumber.pokedex_number <= end) \
        .all()

    ids = []
    for result in id_results:
        ids.append(result.id)

    return session.query(Pokemon) \
        .join(PokemonSpecies, PokemonSpecies.id == Pokemon.species_id) \
        .filter(Pokemon.is_default.is_(True)) \
        .filter(PokemonSpecies.id.in_(ids)) \
        .all()


def find_alola_pokemons():
    return list(map(lambda pokemon_form: pokemon_form.pokemon,
                    session.query(PokemonForm).filter(PokemonForm.form_identifier == 'alola').all()))


def find_galar_pokemons():
    return list(map(lambda pokemon_form: pokemon_form.pokemon,
                    session.query(PokemonForm).filter(PokemonForm.form_identifier == 'galar').all()))


def find_default_gen8_pokemons():
    national_pokedex = session.query(Pokedex).filter(Pokedex.identifier == 'national').one()
    species_results = session.query(PokemonSpecies.id) \
        .select_from(PokemonDexNumber) \
        .join(PokemonSpecies, PokemonSpecies.id == PokemonDexNumber.species_id) \
        .join(Pokedex, PokemonDexNumber.pokedex_id == national_pokedex.id) \
        .filter(PokemonDexNumber.pokedex_number >= 1) \
        .filter(PokemonDexNumber.pokedex_number <= 898) \
        .filter(Pokedex.id == national_pokedex.id) \
        .filter(PokemonDexNumber.pokedex_number.in_(get_default_gen8_national_dex_pokemon_number())) \
        .all()

    species_ids = []
    for result in species_results:
        species_ids.append(result.id)

    return session.query(Pokemon).join(PokemonSpecies, PokemonSpecies.id == Pokemon.species_id).filter(
        Pokemon.is_default.is_(True)).filter(PokemonSpecies.id.in_(species_ids))


def find_pokemon_by_identifier(name: str) -> Pokemon:
    return session.query(Pokemon).filter(Pokemon.identifier == name).one()


# noinspection PyUnresolvedReferences
def find_pokemon_with_specific_page(start_at: int) -> OrderedDict:
    national_dex = session.query(Pokedex).filter(Pokedex.identifier == 'national').one()
    species_results = session.query(PokemonSpecies.id) \
        .select_from(PokemonDexNumber) \
        .join(PokemonSpecies, PokemonSpecies.id == PokemonDexNumber.species_id) \
        .join(Pokedex, PokemonDexNumber.pokedex_id == national_dex.id) \
        .filter(PokemonDexNumber.pokedex_number >= start_at) \
        .filter(Pokedex.id == national_dex.id) \
        .all()

    species_ids = []
    for result in species_results:
        species_ids.append(result.id)

    availabilities = session.query(PokemonMoveAvailability) \
        .join(Pokemon).order_by(Pokemon.id.desc()).filter(PokemonMoveAvailability.has_pokepedia_page.is_(True)).all()

    pokemons = {}

    for availability in availabilities:
        if availability.pokemon.species.id in species_ids:
            pokemons[availability.pokemon.id] = availability.pokemon

    # noinspection PyTypeChecker
    pokemons = OrderedDict(sorted(pokemons.items()))
    return pokemons


def is_pokemon_available_in_version_groups(pkm: Pokemon, vgs: list):
    return session.query(PokemonMoveAvailability) \
        .join(PokemonMoveAvailability.version_group) \
        .join(PokemonMoveAvailability.pokemon) \
        .filter(PokemonMoveAvailability.pokemon_id == pkm.id) \
        .filter(VersionGroup.identifier.in_([vg.identifier for vg in vgs])) \
        .all()


def find_availability_by_pkm_and_form(name: str, vg: VersionGroup) -> PokemonMoveAvailability:
    return session.query(PokemonMoveAvailability) \
        .filter(PokemonMoveAvailability.version_group_id == vg.id) \
        .join(PokemonMoveAvailability.pokemon) \
        .filter(Pokemon.identifier == name) \
        .filter(PokemonMoveAvailability.version_group_id == vg.id) \
        .one()


def get_availability_by_pokemon_and_version_group(pkm: Pokemon,
                                                  vg: VersionGroup) -> PokemonMoveAvailability:
    return session.query(PokemonMoveAvailability) \
        .filter(PokemonMoveAvailability.version_group_id == vg.id) \
        .join(PokemonMoveAvailability.pokemon) \
        .filter(Pokemon.identifier == pkm.identifier) \
        .filter(PokemonMoveAvailability.version_group_id == vg.id) \
        .one_or_none()


# noinspection PyUnresolvedReferences
def find_moves_by_pokemon_move_method_and_version_group(pkm: Pokemon, pkm_move_method: PokemonMoveMethod,
                                                        vg: VersionGroup):
    return session.query(PokemonMove) \
        .join(PokemonMove.version_group) \
        .join(PokemonMove.pokemon) \
        .filter(Pokemon.id == pkm.id) \
        .filter(PokemonMove.pokemon_move_method_id == pkm_move_method.id) \
        .filter(VersionGroup.id == vg.id) \
        .order_by(PokemonMove.level.asc()) \
        .all()


# noinspection PyUnresolvedReferences
def find_moves_by_pokemon_move_method_and_version_groups(pkm: Pokemon, pkm_move_method: PokemonMoveMethod,
                                                         vgs_identifier: list):
    return session.query(PokemonMove) \
        .join(PokemonMove.version_group) \
        .join(PokemonMove.pokemon) \
        .filter(Pokemon.id == pkm.id) \
        .filter(PokemonMove.pokemon_move_method_id == pkm_move_method.id) \
        .filter(VersionGroup.identifier.in_(vgs_identifier)) \
        .order_by(VersionGroup.identifier) \
        .all()


def find_moves_by_pokemon_move_method_and_version_groups_with_concat(pkm: Pokemon, pkm_move_method: PokemonMoveMethod,
                                                                     vgs_identifier: list):
    return session.query(Move, sqlite.group_concat_sqlite(VersionGroup.identifier, '/')) \
        .join(PokemonMove.version_group) \
        .join(PokemonMove.pokemon) \
        .join(PokemonMove.move) \
        .filter(Pokemon.id == pkm.id) \
        .filter(PokemonMove.pokemon_move_method_id == pkm_move_method.id) \
        .filter(VersionGroup.identifier.in_(vgs_identifier)) \
        .group_by(Move.identifier) \
        .all()


def get_french_move_by_pokemon_move_and_generation(pokemon_move: PokemonMove, gen: Generation):
    move = session.query(Move) \
        .filter(Move.id == pokemon_move.move_id).one()

    alias = session.query(MoveNameChangelog) \
        .join(MoveNameChangelog.language) \
        .join(MoveNameChangelog.generation) \
        .join(MoveNameChangelog.move) \
        .filter(Language.iso639 == 'fr') \
        .filter(move.id == Move.id) \
        .filter(Generation.identifier == gen.identifier).first()  # type: MoveNameChangelog

    return {
        'name': move.name_map[languagehelper.french],
        'alias': alias.name if alias else None
    }


def get_french_move_name_by_move_and_generation(move: Move, gen: Generation):
    alias = session.query(MoveNameChangelog) \
        .join(MoveNameChangelog.language) \
        .join(MoveNameChangelog.generation) \
        .join(MoveNameChangelog.move) \
        .filter(Language.iso639 == 'fr') \
        .filter(move.id == Move.id) \
        .filter(Generation.identifier == gen.identifier).first()  # type: MoveNameChangelog

    return {
        'name': move.name_map[languagehelper.french],
        'alias': alias.name if alias else None
    }


def find_french_move_by_move_and_generation(move: Move, generation: int):
    alias = session.query(MoveNameChangelog) \
        .join(Move, Move.id == MoveNameChangelog.move_id) \
        .join(Language, Language.identifier == 'fr') \
        .filter(MoveNameChangelog.generation.identifier ==
                generationhelper.gen_int_to_id(generation)).first()  # type: MoveNameChangelog

    if alias:
        return alias.name

    # noinspection PyUnresolvedReferences
    return move.name_map['fr']


def find_pokepedia_move_methods_methods_repository() -> list:
    return session.query(PokemonMoveMethod).filter(
        PokemonMoveMethod.identifier.in_(['level-up', 'tutor', 'machine', 'egg'])).all()


def find_highest_version_group_by_generation(generation) -> VersionGroup:
    if isinstance(generation, int):
        generation = session.query(Generation).filter(Generation.identifier == generationhelper.gen_int_to_id(
            generation)).one()
    version_groups = session.query(VersionGroup) \
        .filter(VersionGroup.identifier.notin_(['colosseum', 'xd', 'lets-go-pikachu-lets-go-eevee'])) \
        .filter(VersionGroup.generation_id == generation.id) \
        .all()  # type: list

    if len(version_groups) == 1:
        return version_groups[0]

    return functools.reduce(lambda a, b: a if a.order > b.order else b, version_groups)


def find_version_group_identifier_by_generation(generation, step: int) -> list:
    if isinstance(generation, int):
        generation = session.query(Generation).filter(Generation.identifier == generationhelper.gen_int_to_id(
            generation)).one()
    filter = ['colosseum', 'xd']
    if generationhelper.gen_to_int(generation) == 7 and step == 1:
        filter.append('lets-go-pikachu-lets-go-eevee')
    if generationhelper.gen_to_int(generation) == 7 and step == 2:
        filter.append('sun-moon')
        filter.append('ultra-sun-ultra-moon')
    version_groups = session.query(VersionGroup.identifier) \
        .filter(VersionGroup.identifier.notin_(filter)) \
        .filter(VersionGroup.generation_id == generation.id) \
        .all()  # type: list

    vgs = []
    for vg in version_groups:
        vgs.append(vg.identifier)
    return vgs


def find_french_slot1_name_by_gen(pokemon: Pokemon, generation: Generation) -> str:
    type_past = session.query(PokemonTypePast) \
        .join(PokemonTypePast.pokemon) \
        .join(PokemonTypePast.generation) \
        .filter(Pokemon.id == pokemon.id) \
        .filter(generation.id <= Generation.id) \
        .filter(PokemonTypePast.slot == 1) \
        .first()

    if type_past:
        return type_past.type.name_map[languagehelper.french]

    pokemon_type = session.query(PokemonType) \
        .filter(PokemonType.pokemon_id == pokemon.id) \
        .filter(PokemonType.slot == 1).one()

    return session.query(Type).filter(Type.id == pokemon_type.type_id).one().name_map[languagehelper.french]


def get_item_from_cache(key: str, func):
    item = session.query(CacheItem) \
        .filter(CacheItem.key == key) \
        .one_or_none()

    if item:
        return item.data

    result = func()
    item = CacheItem()
    item.key = key
    item.data = result
    session.add(item)
    session.commit()
    return result


def find_pokemon_by_french_form_name(original_pokemon: Pokemon, name: str):
    # noinspection PyUnresolvedReferences
    specific_case = specificcasehelper.is_specific_pokemon_form_name(name)
    if specific_case:
        return specific_case
    form_name_table = PokemonForm.names_table
    form_name_entities = session \
        .query(form_name_table) \
        .filter(form_name_table.form_name == name) \
        .all()
    if len(form_name_entities) == 0:
        form_name_entity = session \
            .query(form_name_table) \
            .filter(form_name_table.pokemon_name == name.title()) \
            .one_or_none()
        if not form_name_entity:
            raise RuntimeError('form not found for name {}'.format(name))
        else:
            return session.query(PokemonForm).filter(
                PokemonForm.id == form_name_entity.pokemon_form_id).one().pokemon
    elif len(form_name_entities) == 1:
        return session.query(PokemonForm).filter(PokemonForm.id == form_name_entities[0].pokemon_form_id).one().pokemon
    else:
        # cheniselle
        for form_name_entity in form_name_entities:
            form_entity = session \
                .query(PokemonForm) \
                .filter(PokemonForm.id == form_name_entity.pokemon_form_id) \
                .one()  # type: PokemonForm
            # noinspection PyUnresolvedReferences
            if form_entity.pokemon.species_id == original_pokemon.species_id:
                # noinspection PyUnresolvedReferences
                return form_entity.pokemon
    raise RuntimeError('form not found for name {}'.format(name))


def find_minimal_pokemon_in_evolution_chain(pkm: Pokemon, gen: Generation):
    if pkm.species.evolves_from_species_id == None:
        return pkm

    evolution_chain_species = pkm.species.evolution_chain.species

    for specy in evolution_chain_species:
        if specy.generation_id <= gen.id and specy.evolves_from_species_id == None:
            return specy.default_pokemon

    raise RuntimeError(f'No specy in evol chain found for pokemon : {pkm.identifier}')

def find_pokemon_learning_move_by_egg_groups(pokemon: Pokemon, move: Move, generation: int, step: int):
    filtersvg = []
    if generation == 7 and step == 1:
        filtersvg.append('lets-go-pikachu-lets-go-eevee')
    if generation == 7 and step == 2:
        filtersvg.append('sun-moon')
        filtersvg.append('ultra-sun-ultra-moon')
    pkmmoves = session.query(PokemonMove) \
        .join(Pokemon) \
        .join(VersionGroup) \
        .join(PokemonSpecies, Pokemon.species_id == PokemonSpecies.id) \
        .filter(PokemonMove.move_id == move.id) \
        .filter(PokemonSpecies.generation_id <= generation) \
        .filter(VersionGroup.generation_id == generation) \
        .filter(VersionGroup.identifier.notin_(filtersvg)) \
        .all()

    return _build_pkm_parent_tree(pokemon, pkmmoves)

def _is_breedable(specy: PokemonSpecies):
    return specy.egg_groups[0].identifier not in ['no-eggs', 'indeterminate']




def _build_pkm_parent_tree(pokemon: Pokemon, pkmmoves: dict):

    egggroups = pokemon.species.egg_groups
    egggroupidentifiers = []
    for group in egggroups:
        egggroupidentifiers.append(group.identifier)

    pkmsandvgs = \
        {
            'machine': {},
            'egg': {},
            'level-up': {},
            'tutor': {}
        }

    for pokemonmove in pkmmoves:
        # if specy order in not present if the list create an entry
        if pokemonmove.pokemon.species.order not in pkmsandvgs[pokemonmove.method.identifier]:
            pkmsandvgs[pokemonmove.method.identifier][pokemonmove.pokemon.species.order] = {}
        # init the skip variable
        skip = False
        evoltrigger = False
        # remove unwanted parent in the list ( mega ... )
        if pokemonmove.pokemon.id > 10000 and not (
                pokemonmove.pokemon.forms[0].form_identifier == 'alola'
                or pokemonmove.pokemon.forms[0].form_identifier == 'galar'
                or pokemonmove.pokemon.forms[0].form_identifier == 'hisui'):
            continue

        # if pokemon.species in pokemonmove.pokemon.species.evolution_chain.species:
        #     skip = True
        # remove pokemon not in egg groups
        if not any(x in pokemonmove.pokemon.species.egg_groups for x in egggroups):
            skip = True
        if pokemonmove.pokemon.identifier not in pkmsandvgs[pokemonmove.method.identifier][
            pokemonmove.pokemon.species.order] and not skip:

            # add all the evolution family in case of egg method
            if pokemonmove.method.identifier == 'egg':
                for specy in pokemonmove.pokemon.species.evolution_chain.species:
                    if not _is_actual_specy_or_evolution(specy,
                                                         pokemonmove.pokemon.species,
                                                         pokemonmove.pokemon.species.evolution_chain.species):
                        continue
                    if specy.order not in pkmsandvgs[pokemonmove.method.identifier]:
                        pkmsandvgs[pokemonmove.method.identifier][specy.order] = {}
                    if not _is_breedable(specy):
                        continue
                    pkmsandvgs['egg'][specy.order][specy.default_pokemon.identifier] = \
                        {
                            "pokemon": specy.default_pokemon,
                            "version_groups": [pokemonmove.version_group]
                        }
                evoltrigger = False
            # if pokemon is allowed to be a parent
            elif _is_breedable(pokemonmove.pokemon.species):
                pkmsandvgs[pokemonmove.method.identifier][pokemonmove.pokemon.species.order][
                    pokemonmove.pokemon.identifier] = \
                    {
                        "pokemon": pokemonmove.pokemon,
                        "version_groups": [pokemonmove.version_group]
                    }
        # if the entry order exist + pokemon exist we must add the new version group
        elif not skip:
            # add the whole family if not present cause its egg method
            if pokemonmove.method.identifier == 'egg':
                for specy in pokemonmove.pokemon.species.evolution_chain.species:
                    if not _is_actual_specy_or_evolution(specy,pokemonmove.pokemon.species,
                                                         pokemonmove.pokemon.species.evolution_chain.species):
                        continue
                    if specy.order not in pkmsandvgs[pokemonmove.method.identifier]:
                        pkmsandvgs[pokemonmove.method.identifier][specy.order] = {}
                    if not _is_breedable(specy):
                        continue
                    if pokemonmove.version_group not in pkmsandvgs['egg'][specy.order][
                        specy.default_pokemon.identifier]['version_groups'] and _is_breedable(specy):
                        pkmsandvgs['egg'][specy.order][specy.default_pokemon.identifier]['version_groups'].append(
                            pokemonmove.version_group)
                evoltrigger = False
            else:
                if pokemonmove.version_group not in \
                        pkmsandvgs[pokemonmove.method.identifier][pokemonmove.pokemon.species.order][
                            pokemonmove.pokemon.identifier]['version_groups'] and _is_breedable(
                    pokemonmove.pokemon.species):
                    pkmsandvgs[pokemonmove.method.identifier][pokemonmove.pokemon.species.order][
                        pokemonmove.pokemon.identifier]['version_groups'].append(
                        pokemonmove.version_group)
        skip = False
        #delete empty entries if no condition where met to add a pokemon in the specy order
        if len(pkmsandvgs[pokemonmove.method.identifier][pokemonmove.pokemon.species.order]) == 0:
            del pkmsandvgs[pokemonmove.method.identifier][pokemonmove.pokemon.species.order]

    # clear
    for methodname, parentbymethod in pkmsandvgs.items():
        copy = {}
        for order, parent in parentbymethod.items():
            if len(parent) != 0:
                copy[order] = parent
        pkmsandvgs[methodname] = copy
    return pkmsandvgs

def _is_actual_specy_or_evolution(specy, mainspecy, species):
    speciesIdentifiers = [element.identifier for element in species]
    if specy.identifier in speciesIdentifiers[speciesIdentifiers.index(mainspecy.identifier):]:
        return True
    else:
        return False
