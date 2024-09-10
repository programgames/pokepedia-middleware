from middleware.models import PokemonMoveAvailability, MoveNameChangelog, CacheItem
from middleware.util.helper import generationhelper, specificcasehelper
from collections import OrderedDict, defaultdict
from django.db.models import F, Func

from middleware.util.helper.languagehelper import get_move_french_name, get_type_french_name
from pokeapi.pokemon_v2.models import Pokedex, PokemonDexNumber, Pokemon, VersionGroup, PokemonMove, Move, Generation, \
    PokemonForm, PokemonTypePast, PokemonType, PokemonSpecies, MoveLearnMethod, PokemonFormName, \
    PokemonEggGroup

"""
Contains functions using the repository pattern to encapsulate database requests
"""

DEFAULT_GEN8_NATIONAL_DEX_POKEMON_NUMBERS = {
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
    43, 44, 45, 50, 51, 52, 53, 54, 55, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 72, 73, 77, 78, 79, 80, 81, 82,
    83, 90, 91, 92, 93, 94, 95, 98, 99, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
    117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138,
    139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 163, 164, 169, 170, 171, 172, 173, 174, 175,
    176, 177, 178, 182, 183, 184, 185, 186, 194, 195, 196, 197, 199, 202, 206, 208, 211, 212, 213, 214, 215, 220,
    221, 222, 223, 224, 225, 226, 227, 230, 233, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248,
    249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 263, 264, 270, 271, 272, 273, 274, 275, 278, 279,
    280, 281, 282, 290, 291, 292, 293, 294, 295, 298, 302, 303, 304, 305, 306, 309, 310, 315, 318, 319, 320, 321,
    324, 328, 329, 330, 333, 334, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 355, 356,
    359, 360, 361, 362, 363, 364, 365, 369, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384,
    385, 403, 404, 405, 406, 407, 415, 416, 420, 421, 422, 423, 425, 426, 427, 428, 434, 435, 436, 437, 438, 439,
    440, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 458, 459, 460, 461, 462, 463, 464, 465,
    466, 467, 468, 470, 471, 473, 474, 475, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 494, 506,
    507, 508, 509, 510, 517, 518, 519, 520, 521, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536,
    537, 538, 539, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561,
    562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 582, 583, 584, 587,
    588, 589, 590, 591, 592, 593, 595, 596, 597, 598, 599, 600, 601, 605, 606, 607, 608, 609, 610, 611, 612, 613,
    614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635,
    636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 649, 659, 660, 661, 662, 663, 674, 675, 677, 678,
    679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700,
    701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 721, 722, 723,
    724, 725, 726, 727, 728, 729, 730, 736, 737, 738, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753,
    754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 776, 777,
    778, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800,
    801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822,
    823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844,
    845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866,
    867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888,
    889, 890, 891, 892, 893, 894, 895, 896, 897, 898
}


def get_default_gen8_national_dex_pokemon_number() -> set:
    return DEFAULT_GEN8_NATIONAL_DEX_POKEMON_NUMBERS


def find_default_pokemons_in_national_dex(start: int, end: int):
    national_pokedex = Pokedex.objects.get(name='national')

    species_ids = PokemonDexNumber.objects.filter(
        pokedex=national_pokedex,
        pokedex_number__range=(start, end)
    ).values_list('pokemon_species_id', flat=True)

    return Pokemon.objects.filter(
        is_default=True,
        pokemon_species_id__in=species_ids
    )


def find_alola_pokemons():
    return list(Pokemon.objects.filter(pokemonform__form_name='alola'))


def find_galar_pokemons():
    return list(Pokemon.objects.filter(pokemonform__form_name='galar'))


def find_default_gen8_pokemons():
    national_pokedex = Pokedex.objects.get(name='national')

    species_ids = PokemonDexNumber.objects.filter(
        pokedex=national_pokedex,
        pokedex_number__in=get_default_gen8_national_dex_pokemon_number()
    ).values_list('pokemon_species_id', flat=True)

    return Pokemon.objects.filter(
        is_default=True,
        pokemon_species_id__in=species_ids
    )


def find_pokemon_by_identifier(name: str) -> Pokemon:
    return Pokemon.objects.get(name=name)


def find_pokemon_with_specific_page(start_at: int) -> OrderedDict:
    national_dex = Pokedex.objects.get(name='national')

    species_ids = PokemonDexNumber.objects.filter(
        pokedex=national_dex,
        pokedex_number__gte=start_at
    ).values_list('pokemon_species_id', flat=True)

    availabilities = PokemonMoveAvailability.objects.filter(
        pokemon__pokemon_species__id__in=species_ids,
        has_pokepedia_page=True
    ).select_related('pokemon').order_by('pokemon_id')

    pokemons = OrderedDict(
        (availability.pokemon.id, availability.pokemon) for availability in availabilities
    )

    return pokemons


def is_pokemon_available_in_version_groups(pkm: Pokemon, vgs: list):
    return PokemonMoveAvailability.objects.filter(
        pokemon=pkm,
        version_group__in=vgs
    )


def find_availability_by_pkm_and_form(name: str, vg: VersionGroup) -> PokemonMoveAvailability:
    return PokemonMoveAvailability.objects.get(
        version_group=vg,
        pokemon__name=name
    )


def get_availability_by_pokemon_and_version_group(pkm: Pokemon, vg: VersionGroup) -> PokemonMoveAvailability:
    return PokemonMoveAvailability.objects.filter(
        pokemon=pkm,
        version_group=vg
    ).select_related('pokemon', 'version_group').first()


def find_moves_by_pokemon_move_method_and_version_group(pkm: Pokemon, move_learn_method: MoveLearnMethod,
                                                        vg: VersionGroup):
    return PokemonMove.objects.filter(
        pokemon=pkm,
        move_learn_method=move_learn_method,
        version_group=vg,
    ).exclude(
        level=0,
        pokemon__pokemon_species__evolves_from_species__isnull=True
    ).order_by('level')


def find_moves_by_pokemon_move_method_and_version_groups(pkm: Pokemon, move_learn_method: MoveLearnMethod,
                                                         vgs_identifier: list):
    return PokemonMove.objects.filter(
        pokemon=pkm,
        move_learn_method=move_learn_method,
        version_group__identifier__in=vgs_identifier
    ).order_by('version_group__identifier')


def find_moves_by_pokemon_move_method_and_version_groups_with_concat(pkm: Pokemon, move_learn_method: MoveLearnMethod,
                                                                     vgs_identifier: list):
    return Move.objects.filter(
        pokemonmove__pokemon=pkm,
        pokemonmove__pokemon_move_method__id=move_learn_method.id,  # Use the ID of move_learn_method
        pokemonmove__version_group__identifier__in=vgs_identifier
    ).annotate(
        version_group_identifiers=Func(F('pokemonmove__version_group__identifier'), function='GROUP_CONCAT',
                                       template="%(function)s(%(expressions)s, '/')")
    ).distinct()


def get_french_move_by_pokemon_move_and_generation(pokemon_move: PokemonMove, gen: Generation):
    return get_french_move_name_by_move_and_generation(pokemon_move.move, gen)


def get_french_move_name_by_move_and_generation(move: Move, gen: Generation):
    alias = MoveNameChangelog.objects.filter(
        move=move,
        generation=gen,
        language__iso639='fr'
    ).first()

    return {
        'name': get_move_french_name(move),
        'alias': alias.name if alias else None
    }


def find_french_move_by_move_and_generation(move: Move, generation: int):
    alias = MoveNameChangelog.objects.filter(
        move=move,
        generation__identifier=generationhelper.gen_int_to_name(generation),
        language__identifier='fr'
    ).first()

    return alias.name if alias else get_move_french_name(move)


def find_pokepedia_move_methods_methods_repository() -> list:
    return MoveLearnMethod.objects.filter(
        identifier__in=['level-up', 'tutor', 'machine', 'egg']
    )


def find_highest_version_group_by_generation(generation) -> VersionGroup:
    if isinstance(generation, int):
        generation = Generation.objects.get(
            name=generationhelper.gen_int_to_name(generation)
        )

    version_groups = VersionGroup.objects.filter(
        generation=generation
    ).exclude(
        name__in=['colosseum', 'xd', 'lets-go-pikachu-lets-go-eevee']
    )

    return version_groups.order_by('-order').first()


def find_version_group_identifier_by_generation(generation, step: int) -> list:

    filter_list = ['colosseum', 'xd']

    if generation.id == 7:
        if step == 1:
            filter_list.append('lets-go-pikachu-lets-go-eevee')
        elif step == 2:
            filter_list.extend(['sun-moon', 'ultra-sun-ultra-moon'])

    version_groups = VersionGroup.objects.filter(
        generation=generation
    ).exclude(
        identifier__in=filter_list
    )

    return list(version_groups.values_list('identifier', flat=True))


def find_french_slot1_name_by_gen(pokemon: Pokemon, generation: Generation) -> str:
    type_past = PokemonTypePast.objects.filter(
        pokemon=pokemon,
        generation__id__lte=generation.id,
        slot=1
    ).first()

    if type_past and type_past.generation_id >= generation.id:
        return get_type_french_name(type_past.type)

    pokemon_type = PokemonType.objects.get(
        pokemon=pokemon,
        slot=1
    )

    return get_type_french_name(pokemon_type.type)


def get_item_from_cache(key: str, func):
    cache_item = CacheItem.objects.filter(key=key).first()

    if cache_item:
        return cache_item.data

    result = func()
    cache_item = CacheItem.objects.create(key=key, data=result)
    cache_item.save()
    return result


def find_pokemon_by_french_form_name(original_pokemon: Pokemon, name: str):
    specific_case = specificcasehelper.is_specific_pokemon_form_name(name)
    if specific_case:
        return specific_case

    form_name_entities = PokemonFormName.objects.filter(name=name)

    if not form_name_entities.exists():
        form_name_entity = PokemonFormName.objects.filter(pokemon_name=name.title()).first()
        if not form_name_entity:
            raise RuntimeError(f'Form not found for name {name}')
        return PokemonForm.objects.get(id=form_name_entity.pokemon_form_id).pokemon

    if form_name_entities.count() == 1:
        return PokemonForm.objects.get(id=form_name_entities.first().pokemon_form_id).pokemon

    for form_name_entity in form_name_entities:
        form_entity = PokemonForm.objects.get(id=form_name_entity.pokemon_form_id)
        if form_entity.pokemon.pokemon_species_id == original_pokemon.pokemon_species.id:
            return form_entity.pokemon

    raise RuntimeError(f'Form not found for name {name}')


def find_minimal_pokemon_in_evolution_chain(pkm: Pokemon, gen: Generation) -> Pokemon:
    if pkm.pokemon_species.evolves_from_species_id is None:
        return pkm

    minimal_species = pkm.pokemon_species.evolves_from_species.objects.get(
        generation_id__lte=gen.id,
        evolves_from_species_id__isnull=True
    ).first()

    if minimal_species:
        return minimal_species.default_pokemon

    raise RuntimeError(f'No species found in evolution chain for pokemon: {pkm.id}')


def find_pokemon_learning_move_by_egg_groups(pokemon: Pokemon, move: Move, generation: Generation, step: int):
    filtersvg = []
    if generation.id == 7 and step == 1:
        filtersvg.append('lets-go-pikachu-lets-go-eevee')
    if generation.id == 7 and step == 2:
        filtersvg.extend(['sun-moon', 'ultra-sun-ultra-moon'])

    pkmmoves = PokemonMove.objects.filter(
        move=move,
        pokemon__species__generation_id__lte=generation.id,
        version_group__generation_id=generation.id
    ).exclude(version_group__identifier__in=filtersvg).select_related('pokemon', 'version_group', 'method')

    return _build_pkm_parent_tree(pokemon, pkmmoves)


def _is_breedable(specy: PokemonSpecies) -> bool:
    egg_groups = PokemonEggGroup.objects.get(pokemon_species=specy)
    return egg_groups[0].name in ['no-eggs', 'indeterminate']


def _build_pkm_parent_tree(pokemon: Pokemon, pkmmoves):
    egg_groups = PokemonEggGroup.objects.get(pokemon_species=pokemon.pokemon_species)

    pkmsandvgs = defaultdict(lambda: defaultdict(dict))

    for pokemonmove in pkmmoves:
        species_order = pokemonmove.pokemon.species.order
        method_identifier = pokemonmove.method.name

        skip = False

        # Skip non-relevant forms (mega, etc.) unless they are Alolan, Galarian, or Hisuian forms
        if pokemonmove.pokemon.id > 10000 and not (
                pokemonmove.pokemon.forms.filter(form_identifier__in=['alola', 'galar', 'hisui']).exists()):
            continue

        if not any(egg_group in pokemonmove.pokemon.species.egg_groups.values_list('identifier', flat=True)
                   for egg_group in egg_groups):
            skip = True

        if not skip:
            if method_identifier == 'egg':
                for specy in pokemonmove.pokemon.species.evolution_chain.species.all():
                    if not _is_actual_specy_or_evolution(specy, pokemonmove.pokemon.species):
                        continue
                    if not _is_breedable(specy):
                        continue

                    pkmsandvgs['egg'][specy.order][specy.default_pokemon.name] = {
                        "pokemon": specy.default_pokemon,
                        "version_groups": [pokemonmove.version_group]
                    }
            else:
                if _is_breedable(pokemonmove.pokemon.species):
                    pkmsandvgs[method_identifier][species_order][pokemonmove.pokemon.name] = {
                        "pokemon": pokemonmove.pokemon,
                        "version_groups": [pokemonmove.version_group]
                    }

            if pokemonmove.version_group not in pkmsandvgs[method_identifier][species_order][
                pokemonmove.pokemon.name]['version_groups']:
                pkmsandvgs[method_identifier][species_order][pokemonmove.pokemon.name]['version_groups'].append(
                    pokemonmove.version_group)

        if len(pkmsandvgs[method_identifier][species_order]) == 0:
            del pkmsandvgs[method_identifier][species_order]

    return _cleanup_pkm_parent_tree(pkmsandvgs)


def _cleanup_pkm_parent_tree(pkmsandvgs):
    for methodname, parentbymethod in pkmsandvgs.items():
        pkmsandvgs[methodname] = {order: parent for order, parent in parentbymethod.items() if parent}
    return pkmsandvgs


def _is_actual_specy_or_evolution(specy, mainspecy):
    species_identifiers = [element.name for element in mainspecy.evolution_chain.species.all()]
    return specy.name in species_identifiers[species_identifiers.index(mainspecy.name):]

def gen_to_int(generation: Generation) -> int:
    mapping = {
        'generation-i': 1,
        'generation-ii': 2,
        'generation-iii': 3,
        'generation-iv': 4,
        'generation-v': 5,
        'generation-vi': 6,
        'generation-vii': 7,
        'generation-viii': 8,
    }

    return mapping[generation.name]