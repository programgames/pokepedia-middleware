import re
from pathlib import Path
import os
import csv

from middleware.connection.conn import session
from middleware.db.tables import MoveNameChangelog
from middleware.util.helper import generationhelper
from pokeapi.db.tables import Language, Generation, Move


def load_french_aliases():
    header = True
    path = Path(__file__).parent / ('data' + os.sep + 'french_move_alias.csv')

    with open(path, newline='', encoding='utf-8') as csvfile:
        line = csv.reader(csvfile, delimiter=',')
        french = session.query(Language).filter(Language.identifier == 'fr').one()
        for row in line:
            if header:&
                header = False
                continue
            gens = re.findall(r'\d', row[2])
            first_gen = int(gens[0])
            second_gen = int(gens[1])
            move = session.query(Move).filter(Move.identifier == row[0]).one_or_none()
            if not move:
                raise RuntimeError('Move not found : ' + row[0])
            for i in range(first_gen, second_gen + 1):
                generation_identifier = generationhelper.gen_int_to_id(i)
                generation = session.query(Generation).filter(Generation.identifier == generation_identifier).one()
                changelog = MoveNameChangelog()
                changelog.language_id = french.id
                changelog.move_id = move.id
                changelog.generation_id = generation.id
                changelog.name = row[1]
                session.add(changelog)
            session.commit()
