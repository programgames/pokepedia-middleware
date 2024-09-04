def _clean_string(string: str) -> str:
    """
    Cleans the input string by removing or replacing specific substrings.
    """
    return string.replace('N.', '').replace(', ', ' ').replace('<br>', ' ').replace('-', '—').replace('’', '\'')


def compare_moves(pokepedia_moves: dict, database_moves: dict, form_order: dict) -> bool:
    """
    Compares the moves from Poképedia with those from the database for each form.
    """
    for form, moves in database_moves.items():
        # Clean the moves from both sources
        clean_database_moves = list(map(_clean_string, moves))
        clean_pokepedia_moves = list(filter(None, map(_clean_string, pokepedia_moves.get(form + form_order[form], {}).get('moves', []))))

        # Check if the number of moves matches
        if len(clean_database_moves) != len(clean_pokepedia_moves):
            return False

        # Check if all moves match
        for i in range(len(clean_database_moves)):
            if clean_database_moves[i] != clean_pokepedia_moves[i]:
                return False

    return True
