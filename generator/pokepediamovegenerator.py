from pokedex.db.tables import PokemonMoveMethod, Pokemon, Generation

import db.repository as repository
from util.helper import movesethelper, generationhelper


def generate_move_wiki_text(learn_method: PokemonMoveMethod, pokemon: Pokemon, generation: Generation, forms: list,
                            pokepedia_data: dict, pokepedia_pokemon_name: str,form_order: dict):
    generated = ''

    french_slot1_name = repository.find_french_slot1_name_by_gen(pokemon, generation)

    for comment in pokepedia_data['topComments']:
        generated += comment + "\r\n"

    pokepedia_learn_method = movesethelper.get_pokepedia_invoke_learn_method(learn_method)

    if len(forms) == 1:
        for comment in pokepedia_data['forms'][pokepedia_pokemon_name]['topComments']:
            generated += comment + "\r\n"
        generated += "{{"f"#invoke:Apprentissage|{pokepedia_learn_method}|type={french_slot1_name}|génération={generationhelper.get_gen_number_by_identifier(generation.identifier)}|\r\n"

        for move in forms[pokepedia_pokemon_name]:
            generated += move.replace('’', '\'') + '\r\n'
        generated += "}}\r\n"
        for comment in pokepedia_data['forms'][pokepedia_pokemon_name]['botComments']:
            generated += comment + "\r\n"
        return generated

    for form, moves in forms.items():
        form = form + form_order[form]
        generated += "===== " + form + " =====" + '\r\n'
        for comment in pokepedia_data['forms'][form]['topComments']:
            generated += comment + "\r\n"
        generated += "{{"f"#invoke:Apprentissage|{pokepedia_learn_method}|type={french_slot1_name}|génération={generationhelper.get_gen_number_by_identifier(generation.identifier)}|\r\n"

        for move in moves:
            generated += move.replace('’', '\'') + '\r\n'
        generated += "}}\r\n"
        for comment in pokepedia_data['forms'][form]['botComments']:
            generated += comment + "\r\n"
    return generated
