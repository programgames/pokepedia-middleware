import re
from pathlib import Path
import os
import csv

from middleware.models import MoveNameChangelog
from middleware.util.helper import generationhelper
from pokemon_v2.models import Language, Move, Generation


def load_french_aliases():
    header = True
    path = Path(__file__).parent / ('data' + os.sep + 'french_move_alias.csv')

    with open(path, newline='', encoding='utf-8') as csvfile:
        line = csv.reader(csvfile, delimiter=',')
        french = Language.objects.get(identifier='fr')
        for row in line:
            if header:
                header = False
                continue
            gens = re.findall(r'\d', row[2])
            first_gen = int(gens[0])
            second_gen = int(gens[1])
            move = Move.objects.filter(identifier=row[0]).first()
            if not move:
                raise RuntimeError('Move not found : ' + row[0])
            for i in range(first_gen, second_gen + 1):
                generation_identifier = generationhelper.gen_int_to_id(i)
                generation = Generation.objects.get(identifier=generation_identifier)
                changelog = MoveNameChangelog()
                changelog.language_id = french.id
                changelog.move_id = move.id
                changelog.generation_id = generation.id
                changelog.name = row[1]
                changelog.save()