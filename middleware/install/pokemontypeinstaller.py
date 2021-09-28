from pathlib import Path
import os
import csv

from middleware.connection.conn import session
from middleware.db.tables import PokemonTypePast


def load_pokemon_type_past():
    header = True
    path = Path(__file__).parent / ('data' + os.sep + 'pokemon_type_past.csv')

    with open(path, newline='', encoding='utf-8') as csvfile:
        line = csv.reader(csvfile, delimiter=',')
        for row in line:
            if header:
                header = False
                continue
            pokemon_id = int(row[0])
            generation_id = int(row[1])
            type_id = int(row[2])
            slot = int(row[3])

            type_past = PokemonTypePast()
            type_past.type_id = type_id
            type_past.generation_id = generation_id
            type_past.pokemon_id = pokemon_id
            type_past.slot = slot
            session.add(type_past)
        session.commit()
