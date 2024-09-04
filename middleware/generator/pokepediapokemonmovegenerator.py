import middleware.db.repository as repository
from middleware.util.helper import pokemonmovehelper, generationhelper
from pokeapi.pokemon_v2.models import Pokemon, Generation, MoveLearnMethod


def generate_move_wiki_text(learn_method: MoveLearnMethod, pokemon: Pokemon, generation: Generation,
                            database_data: dict, pokepedia_data: dict, pokepedia_pokemon_name: str,
                            form_order: dict, step: int) -> str:
    generated = []

    french_slot1_name = repository.find_french_slot1_name_by_gen(pokemon, generation)

    # Add top comments
    generated.extend(pokepedia_data['top_comments'])

    # Determine the learn method for Poképedia
    pokepedia_learn_method = pokemonmovehelper.get_pokepedia_invoke_learn_method(
        learn_method, generationhelper.gen_to_int(generation), step
    )

    if len(database_data) == 1:
        generated.extend(_generate_single_form_text(pokemon,
            pokepedia_pokemon_name, pokepedia_data, pokepedia_learn_method,
            french_slot1_name, generation, learn_method, database_data[pokepedia_pokemon_name]
        ))
    else:
        generated.extend(_generate_multiple_forms_text(
            database_data, form_order, generation, learn_method,
            french_slot1_name, pokepedia_learn_method, pokepedia_data
        ))

    # Add bottom comments
    generated.extend(pokepedia_data['bot_comments'])

    return "\r\n".join(generated)


# noinspection DuplicatedCode
def _generate_single_form_text(pokemon, pokepedia_pokemon_name, pokepedia_data, pokepedia_learn_method,
                               french_slot1_name, generation, learn_method, moves) -> list:
    generated = []

    # Add form-specific top comments
    generated.extend(pokepedia_data['forms'][pokepedia_pokemon_name]['top_comments'])

    # Begin the learn method block
    generated.append(f"{{{{#invoke:Apprentissage|{pokepedia_learn_method}|type={french_slot1_name}|"
                     f"génération={generationhelper.gen_name_to_gen_number(generation.name)}|")

    # Special case for Queulorior
    if learn_method.name == 'egg' and any(group.name == 'monster' for group in pokemon.pokemon_species.egg_groups):
        generated.append('queulorior|')

    # Add moves
    generated.extend(move.replace('’', '\'') for move in moves)
    generated.append("}}")

    # Add form-specific bottom comments
    generated.extend(pokepedia_data['forms'][pokepedia_pokemon_name]['bot_comments'])

    return generated


# noinspection DuplicatedCode
def _generate_multiple_forms_text(database_data, form_order, generation, learn_method,
                                  french_slot1_name, pokepedia_learn_method, pokepedia_data) -> list:
    generated = []

    for form, moves in database_data.items():
        form_key = form + form_order[form]
        header_level = "=====" if 7 <= generationhelper.gen_to_int(generation) <= 8 else "===="
        generated.append(f"{header_level} {form_key} {header_level}")

        # Add form-specific top comments
        generated.extend(pokepedia_data['forms'][form_key]['top_comments'])

        # Begin the learn method block
        generated.append(f"{{{{#invoke:Apprentissage|{pokepedia_learn_method}|type={french_slot1_name}|"
                         f"génération={generationhelper.gen_name_to_gen_number(generation.name)}|")

        # Special case for Queulorior
        if learn_method.name == 'egg' and any(group.name == 'monster' for group in form.species.egg_groups):
            generated.append('queulorior|')

        # Add moves
        generated.extend(move.replace('’', '\'') for move in moves)
        generated.append("}}")

        # Add form-specific bottom comments
        generated.extend(pokepedia_data['forms'][form_key]['bot_comments'])

    return generated

def generate_specific_no_pokemon_machine_move_wikitext(pokemon: Pokemon, generation: Generation, step: int) -> str:
    french_slot1_name = repository.find_french_slot1_name_by_gen(pokemon, generation)
    pokepedia_learn_method = 'capsule' if generationhelper.gen_to_int(generation) == 8 and step == 2 else 'disque'

    return f"{{{{#invoke:Apprentissage|{pokepedia_learn_method}|type={french_slot1_name}|génération={generationhelper.gen_name_to_gen_number(generation.name)}|Aucune|}}}}"
