from django.core.exceptions import ObjectDoesNotExist
import middleware.db.repository as repository
from pokeapi.pokemon_v2.models import Generation, VersionGroup, Pokemon

""" Provide tools to deal with generations
"""

def check_if_pokemon_has_move_availability_in_generation(pokemon: Pokemon, generation: Generation) -> bool:
    version_groups = VersionGroup.objects.filter(generation=generation)
    availabilities = repository.is_pokemon_available_in_version_groups(pokemon, version_groups)
    return availabilities.exists()


def check_if_pokemon_is_available_in_lgpe(pokemon: Pokemon) -> bool:
    try:
        version_group = VersionGroup.objects.get(name='lets-go-pikachu-lets-go-eevee')
    except ObjectDoesNotExist:
        return False

    availabilities = repository.is_pokemon_available_in_version_groups(pokemon, [version_group])
    return availabilities.exists()
