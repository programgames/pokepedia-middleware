from middleware.api.pokepedia import pokepedia_client
from middleware.connection.conn import session
from middleware.db import repository
from middleware.db.tables import PokemonMoveAvailability
from middleware.exception import PokemonMoveException, NoMachineMoveLearnAndNoTemplateException, \
    MissingMachineMoveTemplateException, InvalidConditionException, MissingEggMoveTemplateException
from middleware.generator import pokepediapokemonmovegenerator
from middleware.provider.database import pokemonmoveprovider
from middleware.util.helper import generationhelper, languagehelper
from pokeapi.db import util
from pokeapi.db.tables import Generation, Pokemon, PokemonMoveMethod, VersionGroup


def handlerpokemonmoveerror(exc: PokemonMoveException, pokemon: Pokemon, generation: Generation, step: int,
                            pokepedia_pokemon_name: str):
    if isinstance(exc, NoMachineMoveLearnAndNoTemplateException):
        if not exc.additional_data['wikitext']:
            generated = pokepediapokemonmovegenerator.generate_specific_no_pokemon_machine_move_wikitext(pokemon,
                                                                                                         generation,
                                                                                                         step)
            print('Uploading correction')
            pokepedia_client.upload(exc.additional_data['section'], exc.additional_data['page'], generated,
                                    'Mis a jour des attaques apprises')
            return
    elif isinstance(exc, MissingMachineMoveTemplateException):
        if not exc.additional_data['wikitext']:
            machine = util.get(session, PokemonMoveMethod, 'machine')
            if not _has_multiple_forms_for_machine_moves(generation, step, pokemon):
                specy = pokemon.species
                specy_name = specy.name_map[languagehelper.french].replace(' ', '_')  # M. Mime
                form_order = {specy_name: ''}
                if generationhelper.gen_to_int(generation) > 6:
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
                database_moves = pokemonmoveprovider.get_database_pokemon_moves(pokemon, generation, machine,
                                                                                form_order, step)
                generated = pokepediapokemonmovegenerator.generate_move_wiki_text(machine, pokemon, generation,
                                                                                  database_moves, pokepedia_data,
                                                                                  pokepedia_pokemon_name, form_order,
                                                                                  step)
                print('Uploading correction')
                pokepedia_client.upload(exc.additional_data['section'], exc.additional_data['page'], generated,
                                        'Mis a jour des attaques apprises')
                return
    elif isinstance(exc, MissingEggMoveTemplateException):
        if not exc.additional_data['wikitext']:
            specy = pokemon.species
            specy_name = specy.name_map[languagehelper.french].replace(' ', '_')  # M. Mime
            egg = util.get(session, PokemonMoveMethod, 'egg')

            form_order = {specy_name: ''}
            if generationhelper.gen_to_int(generation) > 6:
                raise exc
            pokepedia_data = {
                'top_comments': ['=== Par [[reproduction]] ==='],
                'forms': {
                    pokepedia_pokemon_name: {
                        'top_comments': [],
                        'bot_comments': []
                    },
                },
                'bot_comments': []
            }
            database_moves = pokemonmoveprovider.get_database_pokemon_moves(pokemon, generation, egg,
                                                                            form_order, step)
            generated = pokepediapokemonmovegenerator.generate_move_wiki_text(egg, pokemon, generation,
                                                                              database_moves, pokepedia_data,
                                                                              pokepedia_pokemon_name, form_order,
                                                                              step)
            print('Uploading correction')
            pokepedia_client.upload(exc.additional_data['section'], exc.additional_data['page'], generated,
                                    'Mis a jour des attaques apprises')
            return


def _has_multiple_forms_for_machine_moves(generation: Generation, step: int, pokemon: Pokemon):
    gen_number = generationhelper.gen_to_int(generation)
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

    return has_multiple_form_for_move_method
