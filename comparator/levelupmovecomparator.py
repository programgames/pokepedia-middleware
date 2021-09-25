def _clean_string(string: str):
    return string.replace('N.', '').replace(', ', ' ').replace('<br>', ' ').replace('-', '—').replace('’', '\'')


def compare_level_move(pokepedia_moves: dict, database_moves: dict) -> bool:
    for form, moves in database_moves.items():

        clean_database_moves = list(map(_clean_string, moves))
        clean_pokepedia_moves = list(map(_clean_string, pokepedia_moves[form]['moves']))

        count = len(clean_database_moves)
        if count != len(clean_pokepedia_moves):
            return False
        for i in range(0, count):
            if clean_database_moves[i] not in clean_pokepedia_moves or clean_pokepedia_moves[
                i] not in clean_database_moves:
                return False
        for i in range(0, count):
            if clean_pokepedia_moves[i] != clean_database_moves[i]:
                return False

    return True
