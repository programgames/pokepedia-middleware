from pokedex.db.tables import PokemonMoveMethod, Pokemon, Generation

import middleware.db.repository as repository
from middleware.util.helper import pokemonmovehelper, generationhelper


def generate_move_wiki_text(learn_method: PokemonMoveMethod, pokemon: Pokemon, generation: Generation, forms: dict,
                            pokepedia_data: dict, pokepedia_pokemon_name: str, form_order: dict, step: int):
    generated = ''

    french_slot1_name = repository.find_french_slot1_name_by_gen(pokemon, generation)

    for comment in pokepedia_data['top_comments']:
        generated += comment + "\r\n"

    pokepedia_learn_method = pokemonmovehelper.get_pokepedia_invoke_learn_method(learn_method,
                                                                                 generationhelper.gen_to_int(
                                                                                     generation), step)

    if len(forms) == 1:
        for comment in pokepedia_data['forms'][pokepedia_pokemon_name]['top_comments']:
            generated += comment + "\r\n"
        generated += "{{"f"#invoke:Apprentissage|{pokepedia_learn_method}|type={french_slot1_name}|" \
                     f"génération={generationhelper.gen_id_to_int(generation.identifier)}|\r\n"

        # noinspection PyTypeChecker
        for move in forms[pokepedia_pokemon_name]:
            generated += move.replace('’', '\'') + '\r\n'
        generated += "}}\r\n"
        for comment in pokepedia_data['forms'][pokepedia_pokemon_name]['bot_comments']:
            generated += comment + "\r\n"
        return generated

    for form, moves in forms.items():
        form = form + form_order[form]
        if 7 <= generationhelper.gen_to_int(generation) <= 8:
            generated += "===== " + form + " =====" + '\r\n'
        else:
            generated += "==== " + form + " ====" + '\r\n'
        for comment in pokepedia_data['forms'][form]['top_comments']:
            generated += comment + "\r\n"
        generated += "{{"f"#invoke:Apprentissage|{pokepedia_learn_method}|type={french_slot1_name}|" \
                     f"génération={generationhelper.gen_id_to_int(generation.identifier)}|\r\n"

        for move in moves:
            generated += move.replace('’', '\'') + '\r\n'
        generated += "}}\r\n"
        for comment in pokepedia_data['forms'][form]['bot_comments']:
            generated += comment + "\r\n"
    return generated


def generate_specific_no_pokemon_machine_move_wikitext(pokemon: Pokemon, generation: Generation, step: int):
    generated = ''

    french_slot1_name = repository.find_french_slot1_name_by_gen(pokemon, generation)

    if generationhelper.gen_to_int(generation) == 8 and step == 2:
        pokepedia_learn_method = 'capsule'
    else:
        pokepedia_learn_method = 'disque'

    generated += "{{"f"#invoke:Apprentissage|{pokepedia_learn_method}|type={french_slot1_name}|" \
                 f"génération={generationhelper.gen_id_to_int(generation.identifier)}|Aucune|}}"

    return generated
