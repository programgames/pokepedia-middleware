from middleware.api.pokepedia import pokepedia_client
from middleware.db import repository
from middleware.exception import (
    PokemonMoveException,
    NoMachineMoveLearnAndNoTemplateException,
    MissingMachineMoveTemplateException,
    InvalidConditionException,
    MissingEggMoveTemplateException
)
from middleware.generator.pokemonmove import pokepediapokemonmovegenerator
from middleware.models import PokemonMoveAvailability
from middleware.provider.database import pokemonmoveprovider
from middleware.util.helper.languagehelper import get_pokemon_specy_french_name
from pokeapi.pokemon_v2.models import Pokemon, Generation, VersionGroup, MoveLearnMethod


# noinspection DuplicatedCode
def handlerpokemonmoveerror(exc: PokemonMoveException, pokemon: Pokemon, generation: Generation, step: int,
                            pokepedia_pokemon_name: str):
    if isinstance(exc, NoMachineMoveLearnAndNoTemplateException):
        if not exc.additional_data['wikitext']:
            generated = pokepediapokemonmovegenerator.generate_specific_no_pokemon_machine_move_wikitext(
                pokemon, generation, step
            )
            print('Uploading correction')
            pokepedia_client.upload(
                exc.additional_data['section'], exc.additional_data['page'], generated,
                'Mise à jour des attaques apprises'
            )
            return

    elif isinstance(exc, MissingMachineMoveTemplateException):
        if not exc.additional_data['wikitext']:
            machine = MoveLearnMethod.objects.get(name='machine')
            if not _has_multiple_forms_for_machine_moves(generation, step, pokemon):
                specy_name = get_pokemon_specy_french_name(pokemon.pokemon_species).replace(' ', '_')
                if generation.id > 6:
                    # too specific as i remember with specific case, better to do it manually ?
                    raise exc
                pokepedia_data = {
                    'top_comments': ['=== Par [[CT]]/[[CS]] ==='],
                    'forms': {
                        pokepedia_pokemon_name: {
                            'top_comments': [],
                            'bot_comments': []
                        }
                    }
                }
                database_moves = pokemonmoveprovider.get_database_pokemon_moves(
                    pokemon, generation, machine, {specy_name: ''}, step
                )
                generated = pokepediapokemonmovegenerator.generate_move_wiki_text(
                    machine, pokemon, generation, database_moves, pokepedia_data,
                    pokepedia_pokemon_name, {specy_name: ''}, step
                )
                print('Uploading correction')
                pokepedia_client.upload(
                    exc.additional_data['section'], exc.additional_data['page'], generated,
                    'Mise à jour des attaques apprises'
                )
                return

    elif isinstance(exc, MissingEggMoveTemplateException):
        if not exc.additional_data['wikitext']:
            egg = MoveLearnMethod.objects.get(name='egg')
            specy_name = get_pokemon_specy_french_name(pokemon.pokemon_species).replace(' ', '_')
            # too specific as i remember with specific case, better to do it manually ?
            if generation.id > 6:
                raise exc
            pokepedia_data = {
                'top_comments': ['=== Par [[reproduction]] ==='],
                'forms': {
                    pokepedia_pokemon_name: {
                        'top_comments': [],
                        'bot_comments': []
                    }
                },
                'bot_comments': []
            }
            database_moves = pokemonmoveprovider.get_database_pokemon_moves(
                pokemon, generation, egg, {specy_name: ''}, step
            )
            generated = pokepediapokemonmovegenerator.generate_move_wiki_text(
                egg, pokemon, generation, database_moves, pokepedia_data,
                pokepedia_pokemon_name, {specy_name: ''}, step
            )
            print('Uploading correction')
            pokepedia_client.upload(
                exc.additional_data['section'], exc.additional_data['page'], generated,
                'Mise à jour des attaques apprises'
            )
            return


def _has_multiple_forms_for_machine_moves(generation: Generation, step: int, pokemon: Pokemon) -> bool:

    if 1 <= generation.id <= 6 or generation.id == 8:
        version_group = repository.find_highest_version_group_by_generation(generation)
    elif generation.id == 7:
        if step == 1 and pokemon.name not in ['meltan', 'melmetal']:
            version_group = VersionGroup.objects.get(name='ultra-sun-ultra-moon')
        else:
            version_group = VersionGroup.objects.get(name='lets-go-pikachu-lets-go-eevee')
    else:
        raise InvalidConditionException(f'Invalid generation/step condition: {generation.id} / {step}')

    availability = PokemonMoveAvailability.objects.filter(
        version_group=version_group,
        pokemon=pokemon,
        has_pokepedia_page=True
    ).first()

    return availability and availability.forms and availability.forms[0].machine
