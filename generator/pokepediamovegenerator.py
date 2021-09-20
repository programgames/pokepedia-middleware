import re

from pokedex.db.tables import PokemonMoveMethod, Pokemon

import db.repository as repository
from util.helper import movesethelper


def generate_move_wiki_text(learn_method: PokemonMoveMethod, pokemon: Pokemon, generation: int, moves: list,
                            pokepedia_data):
    generated = ''

    if commentaries:
        for commentary in commentaries:
            generated += commentary + "\r\n"
        generated += "\r\n"

    french_slot1_name = repository.find_french_slot1_name_by_gen(pokemon, generation)
    pokepedia_learn_method = movesethelper.get_pokepedia_invoke_learn_method(learn_method)

    temp = "{{#invoke:Apprentissage|{}|type={}|génération={}|" + "\r\n"
    generated += temp.format(pokepedia_learn_method, french_slot1_name, generation)

    for move in moves:
        generated += move + "\r\n"

    generated += "}}"

    return generated