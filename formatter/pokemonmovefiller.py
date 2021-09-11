from pokedex.db.tables import PokemonMove

from formatter.dto.levelupmove import LevelUpMove


def fill_leveling_move(move: LevelUpMove, column: int, name: str, pokemon_move_entity: PokemonMove) -> LevelUpMove:
    setattr(move, 'name' + str(column), name)
    level = pokemon_move_entity.level
    if level == 1:
        setattr(move, 'onStart' + str(column), True)
    elif level == 0:
        setattr(move, 'onEvolution' + str(column), True)
    elif getattr(move, 'level' + str(column)) == None:
        setattr(move, 'level' + str(column), level)
    else:
        setattr(move, 'level' + str(column) + 'Extra', level)

    return move
