from django.db import transaction

from middleware.db import repository
from middleware.models import PokemonMoveAvailability
from pokemon_v2.models import VersionGroup

red_blue_vg = VersionGroup.objects.get(identifier='red-blue')
yellow_vg = VersionGroup.objects.get(identifier='yellow')
gold_silver_vg = VersionGroup.objects.get(identifier='gold-silver')
crystal_vg = VersionGroup.objects.get(identifier='crystal')
ruby_sapphir_vg = VersionGroup.objects.get(identifier='ruby-sapphire')
firered_leafgreen_vg = VersionGroup.objects.get(identifier='firered-leafgreen')
emerald_vg = VersionGroup.objects.get(identifier='emerald')
fire_red_leaf_green_vg = VersionGroup.objects.get(identifier='firered-leafgreen')
diamond_pearl_vg = VersionGroup.objects.get(identifier='diamond-pearl')
platinum_vg = VersionGroup.objects.get(identifier='platinum')
heart_gold_soul_silver_vg = VersionGroup.objects.get(identifier='heartgold-soulsilver')
black_white_vg = VersionGroup.objects.get(identifier='black-white')
black2_white2_vg = VersionGroup.objects.get(identifier='black-2-white-2')
xy_vg = VersionGroup.objects.get(identifier='x-y')
oras_vg = VersionGroup.objects.get(identifier='omega-ruby-alpha-sapphire')
sun_moon_vg = VersionGroup.objects.get(identifier='sun-moon')
ultra_sun_ultra_moon_vg = VersionGroup.objects.get(identifier='ultra-sun-ultra-moon')
lgpe_vg = VersionGroup.objects.get(identifier='lets-go-pikachu-lets-go-eevee')
sword_shield_vg = VersionGroup.objects.get(identifier='sword-shield')




def load_basic_move_availabilities():
    save_availabilities(red_blue_vg, 1, 151)
    save_availabilities(yellow_vg, 1, 151)
    save_availabilities(crystal_vg, 1, 251)
    save_availabilities(gold_silver_vg, 1, 251)
    save_availabilities(fire_red_leaf_green_vg, 1, 386)
    save_availabilities(ruby_sapphir_vg, 1, 386)
    save_availabilities(emerald_vg, 1, 386)
    save_availabilities(diamond_pearl_vg, 1, 493)
    save_availabilities(platinum_vg, 1, 493)
    save_availabilities(heart_gold_soul_silver_vg, 1, 493)
    save_availabilities(black_white_vg, 1, 649)
    save_availabilities(black2_white2_vg, 1, 649)
    save_availabilities(xy_vg, 1, 721)
    save_availabilities(oras_vg, 1, 721)
    save_availabilities(sun_moon_vg, 1, 807)
    save_availabilities(ultra_sun_ultra_moon_vg, 1, 807)
    save_alola_pokemons(sun_moon_vg)
    save_alola_pokemons(ultra_sun_ultra_moon_vg)
    save_alola_pokemons(sword_shield_vg, True)
    save_galar_pokemons(sword_shield_vg)
    save_default_gen8_pokemons(sword_shield_vg)
    save_availabilities(lgpe_vg, 1, 151)
    save_availabilities(lgpe_vg, 808, 809)
    save_alola_pokemons(lgpe_vg)


def load_specific_pokemon_move_availabilities():
    # gen 3
    save_pokemon_move_availabilities_with_forms([ruby_sapphir_vg, emerald_vg, firered_leafgreen_vg],
                                                'deoxys-normal', ['deoxys-attack', 'deoxys-defense', 'deoxys-speed'],
                                                False, True, False, False, True)
    # gen4
    save_pokemon_move_availabilities_with_forms([diamond_pearl_vg, platinum_vg, heart_gold_soul_silver_vg],
                                                'deoxys-normal', ['deoxys-attack', 'deoxys-defense', 'deoxys-speed'],
                                                False, True, False, False, True)
    save_pokemon_move_availabilities_with_forms([diamond_pearl_vg, platinum_vg, heart_gold_soul_silver_vg],
                                                'wormadam-plant', ['wormadam-sandy', 'wormadam-trash'],
                                                False, True, True, False, True)
    save_pokemon_move_availabilities_with_forms([platinum_vg, heart_gold_soul_silver_vg, heart_gold_soul_silver_vg],
                                                'shaymin-land', ['shaymin-sky'],
                                                False, True, False, False, True)
    # gen 5
    save_pokemon_move_availabilities_with_forms([black_white_vg, black2_white2_vg],
                                                'deoxys-normal', ['deoxys-attack', 'deoxys-defense', 'deoxys-speed'],
                                                False, True, False, False, True)
    save_pokemon_move_availabilities_with_forms([black_white_vg, black2_white2_vg],
                                                'wormadam-plant', ['wormadam-sandy', 'wormadam-trash'],
                                                False, True, True, False, True)
    save_pokemon_move_availabilities_with_forms([black_white_vg, black2_white2_vg],
                                                'shaymin-land', ['shaymin-sky'],
                                                False, True, False, False, True)
    save_pokemon_move_availabilities_with_forms([black2_white2_vg],
                                                'kyurem', ['kyurem-black', 'kyurem-white'], True)
    # gen6
    # noinspection DuplicatedCode
    save_pokemon_move_availabilities_with_forms([xy_vg, oras_vg],
                                                'meowstic-male', ['meowstic-female'],
                                                False, True, False, False, False)
    save_pokemon_move_availabilities_with_forms([xy_vg, oras_vg],
                                                'deoxys-normal', ['deoxys-attack', 'deoxys-defense', 'deoxys-speed'],
                                                False, True, False, False, True)
    save_pokemon_move_availabilities_with_forms([xy_vg, oras_vg],
                                                'wormadam-plant', ['wormadam-sandy', 'wormadam-trash'],
                                                False, True, True, False, True)
    save_pokemon_move_availabilities_with_forms([xy_vg, oras_vg],
                                                'shaymin-land', ['shaymin-sky'],
                                                False, True, False, False, True)
    save_pokemon_move_availabilities_with_forms([xy_vg, oras_vg],
                                                'kyurem', ['kyurem-black', 'kyurem-white'], True)
    save_pokemon_move_availabilities_with_forms([xy_vg, oras_vg],
                                                'hoopa', ['hoopa-unbound'], False, True, False, False, False)
    # gen7
    # noinspection DuplicatedCode
    save_pokemon_move_availabilities_with_forms([sun_moon_vg, ultra_sun_ultra_moon_vg],
                                                'meowstic-male', ['meowstic-female'],
                                                False, True, False, False, False)
    save_pokemon_move_availabilities_with_forms([sun_moon_vg, ultra_sun_ultra_moon_vg],
                                                'deoxys-normal', ['deoxys-attack', 'deoxys-defense', 'deoxys-speed'],
                                                False, True, False, False, True)
    save_pokemon_move_availabilities_with_forms([sun_moon_vg, ultra_sun_ultra_moon_vg],
                                                'wormadam-plant', ['wormadam-sandy', 'wormadam-trash'],
                                                False, True, True, False, True)
    save_pokemon_move_availabilities_with_forms([sun_moon_vg, ultra_sun_ultra_moon_vg],
                                                'shaymin-land', ['shaymin-sky'],
                                                False, True, False, False, True)
    save_pokemon_move_availabilities_with_forms([sun_moon_vg, ultra_sun_ultra_moon_vg],
                                                'kyurem', ['kyurem-black', 'kyurem-white'], True)
    save_pokemon_move_availabilities_with_forms([sun_moon_vg, ultra_sun_ultra_moon_vg],
                                                'hoopa', ['hoopa-unbound'], False, True, False, False, False)
    save_pokemon_move_availabilities_with_forms([sun_moon_vg],
                                                'lycanroc-midday', ['lycanroc-midnight'],
                                                False, True, False, False, True)
    save_pokemon_move_availabilities_with_forms([ultra_sun_ultra_moon_vg],
                                                'lycanroc-midday', ['lycanroc-midnight', 'lycanroc-dusk'],
                                                False, True, False, False, True)
    save_pokemon_move_availabilities_with_forms([sun_moon_vg, ultra_sun_ultra_moon_vg],
                                                'thundurus-incarnate', ['thundurus-therian'],
                                                False, False, True, False, False)
    save_pokemon_move_availabilities_with_forms([ultra_sun_ultra_moon_vg],
                                                'necrozma', ['necrozma-dusk', 'necrozma-dawn'], True)
    # gen 8
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'meowstic-male', ['meowstic-female'],
                                                False, True, True, False, False)
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'indeedee-male', ['indeedee-female'],
                                                False, True, True, True, False)
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'lycanroc-midday', ['lycanroc-midnight', 'lycanroc-dusk'],
                                                False, True, True, False, True)
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'toxtricity-amped', ['toxtricity-low-key'],
                                                False, True, True, False, True)
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'urshifu-single-strike', ['urshifu-rapid-strike'])
    save_pokemon_move_availabilities_with_forms([sword_shield_vg],
                                                'calyrex', ['calyrex-ice', 'calyrex-shadow'], True)


@transaction.atomic
def save_pokemon_move_availabilities_with_forms(version_groups: list, original_name: str, forms: list,
                                                specific_page_forms=False, level=True, machine=True, egg=True,
                                                tutor=True):
    for version_group in version_groups:
        # Récupération de l'objet original Pokémon Availability
        original_pokemon_availability = repository.find_availability_by_pkm_and_form(original_name, version_group)

        for form in forms:
            # Récupération du Pokémon de la forme
            form_pokemon = repository.find_pokemon_by_identifier(form)

            # Création de l'objet PokemonMoveAvailability
            availability = PokemonMoveAvailability(
                version_group_id=version_group.id,
                pokemon_id=form_pokemon.id,
                has_pokepedia_page=specific_page_forms,
                is_default=False,
                level=level,
                machine=machine,
                egg=egg,
                tutor=tutor
            )
            availability.save()  # Sauvegarde de la disponibilité

            # Ajout de la disponibilité à l'objet original Pokémon Availability
            original_pokemon_availability.forms.add(availability)

        # Sauvegarde des modifications de l'objet original Pokémon Availability
        original_pokemon_availability.save()


def save_availabilities(version_group, start, end):
    pokemons = repository.find_default_pokemons_in_national_dex(start, end)
    with transaction.atomic():
        for pokemon in pokemons:
            move_availability = PokemonMoveAvailability(
                version_group_id=version_group.id,
                pokemon_id=pokemon.id
            )
            move_availability.save()

def save_alola_pokemons(version_group, gen8=False):
    excludeds = [
        'rattata-alola', 'raticate-alola', 'geodude-alola', 'graveler-alola', 'golem-alola', 'grimer-alola', 'muk-alola'
    ]

    pokemons = repository.find_alola_pokemons()
    with transaction.atomic():
        for pokemon in pokemons:
            if gen8 and pokemon.identifier in excludeds:
                continue
            move_availability = PokemonMoveAvailability(
                version_group_id=version_group.id,
                pokemon_id=pokemon.id,
                is_default=False
            )
            move_availability.save()

def save_galar_pokemons(version_group):
    pokemons = repository.find_galar_pokemons()
    with transaction.atomic():
        for pokemon in pokemons:
            move_availability = PokemonMoveAvailability(
                version_group_id=version_group.id,
                pokemon_id=pokemon.id,
                is_default=False
            )
            move_availability.save()


def save_default_gen8_pokemons(version_group):
    pokemons = repository.find_default_gen8_pokemons()

    with transaction.atomic():
        for pokemon in pokemons:
            move_availability = PokemonMoveAvailability(
                version_group_id=version_group.id,
                pokemon_id=pokemon.id
            )
            move_availability.save()
