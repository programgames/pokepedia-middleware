from middleware.util.helper.ormhelper import get_object_or_none
from pokeapi.pokemon_v2.models import Language, Move, PokemonType, TypeName, PokemonSpecies, PokemonForm, Item, Type

french = Language.objects.get(name='fr')

#TODO : verifier si ça prend le bon
def get_move_french_name(move: Move):
    return move.movename.get(language_id=french.id)

def get_type_french_name(type_entity: Type):
    return TypeName.objects.get(language_id=french.id,type=type_entity).name

def get_pokemon_specy_french_name(specy: PokemonSpecies):
    return specy.pokemonspeciesname.get(language_id=french.id)

def get_pokemon_form_french_name(pokemon_form: PokemonForm):
    return pokemon_form.pokemonformname.get(language_id=french.id)

def get_item_french_name(item: Item):
    return item.itemname.get(language_id=french.id)