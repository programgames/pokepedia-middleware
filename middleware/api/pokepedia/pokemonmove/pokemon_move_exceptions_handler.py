from django.core.exceptions import ObjectDoesNotExist

from middleware.exception import MissingEggMoveTemplateException, NoMachineMoveLearnAndNoTemplateException, \
    MissingMachineMoveTemplateException, NoEggMoveLearnAndNoTemplateException
from middleware.util.helper import machinehelper
from middleware.util.helper.pokemonmovehelper import EGG_TYPE, MACHINE_TYPE
from pokeapi.pokemon_v2.models import MoveLearnMethod, PokemonMove
from middleware.db import repository



def handle_template_not_found(exc, method_type, generation, pokemon, moves_data, step):
    try:
        machine_method = MoveLearnMethod.objects.get(name=method_type)
        version = repository.find_highest_version_group_by_generation(generation)

        pkmmoves = PokemonMove.objects.filter(
            version_group_id=version.id,
            pokemon_id=pokemon.id,
            pokemon_move_method_id=machine_method.id
        )

        if method_type == MACHINE_TYPE:
            if step == 2 and generation == 8:
                pkmmoves_number = sum(1 for pkmmove in pkmmoves if machinehelper.is_hm(pkmmove.machine, generation))
            else:
                pkmmoves_number = pkmmoves.count()

            if pkmmoves_number == 0:
                raise NoMachineMoveLearnAndNoTemplateException(
                    f'{pokemon.name} does not learn any moves by machine',
                    {'section': moves_data['section'], 'page': moves_data['page'], 'wikitext': moves_data['wikitext']}
                )
            else:
                raise MissingMachineMoveTemplateException(
                    f'{pokemon.name} is missing a machine move template',
                    {'section': moves_data['section'], 'page': moves_data['page'], 'wikitext': moves_data['wikitext']}
                )

        elif method_type == EGG_TYPE:
            pkmmoves_number = pkmmoves.count()
            if pkmmoves_number == 0:
                raise NoEggMoveLearnAndNoTemplateException(
                    f'{pokemon.name} does not learn any moves by reproduction',
                    {'section': moves_data['section'], 'page': moves_data['page'], 'wikitext': moves_data['wikitext']}
                )
            else:
                raise MissingEggMoveTemplateException(
                    f'{pokemon.name} is missing an egg move template',
                    {'section': moves_data['section'], 'page': moves_data['page'], 'wikitext': moves_data['wikitext']}
                )
    except ObjectDoesNotExist:
        raise exc