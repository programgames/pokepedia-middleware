import re

from exception import WrongHeaderError
from collections import OrderedDict


def check_and_sanitize_moves(moves: list, pokemon_name: str) -> dict:
    template = None
    end = None
    form = None
    actual_form = None
    section = {
        'topComments': [],
        'forms': OrderedDict(),
        'botComments': [],
    }
    if not re.search(r'(\[\[Septième génération]])|(\[\[Huitième génération]])|(Par montée en \[\[niveau]])',
                     moves[0]):
        raise WrongHeaderError('Invalid header: {}'.format(moves[0]))
    section['topComments'].append(moves[0])
    del moves[0]
    r = re.compile(r'.*{{#invoke:Apprentissage\|niveau\|.*')

    templates = len(list(filter(r.match, moves)))
    if templates == 0:
        raise RuntimeError('no level template found')

    forms = OrderedDict()
    if templates == 1:
        forms[pokemon_name] = {
            'topComments': [],
            'forms': OrderedDict(),
            'botComments': [],
        }
        for move in moves:
            if not template and not re.match(r'.*{{#invoke:Apprentissage\|niveau\|.*', move) and not end:
                section['topComments'].append(move)
            elif not template and re.match(r'.*{{#invoke:Apprentissage\|niveau\|.*', move):
                template = True
                end = False
            elif template and re.match(r'^}}$', move):
                template = False
                end = True
            elif end:
                section['botComments'].append(move)
            else:
                if 'moves' not in forms[pokemon_name]:
                    forms[pokemon_name]['moves'] = []
                forms[pokemon_name]['moves'].append(move)
        section['forms'] = forms
        return section

    for move in moves:
        if not template and not form and not bool(re.match(r'.*=.*=.*', move)) and not end:
            section['topComments'].append(move)
        elif not template and form and bool(re.match(r'.*{{#invoke:Apprentissage\|niveau\|.*', move)):
            template = True
            end = False
        elif not template and bool(re.match(r'.*=.*=.*', move)):
            form = True
            end = False
            actual_form = move.strip().replace('=', '').strip()
            forms[actual_form] = {
                'topComments': [],
                'moves': [],
                'botComments': [],
            }
        elif template and re.match(r'.*}}.*', move):
            template = False
            end = True
        elif template and form and not re.match(r'.*}}.*', move):
            forms[actual_form]['moves'].append(move)
        elif form and not re.match('.*=.*=.*', move) and not template and not end:
            forms[actual_form]['topComments'].append(move)
        elif end:
            forms[actual_form]['botComments'].append(move)

    section['forms'] = forms

    return section
