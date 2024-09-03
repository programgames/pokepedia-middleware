import re

from middleware.exception import WrongHeaderError
from collections import OrderedDict

from middleware.exception.exceptions import TemplateNotFoundError

""" Parse , check , and satanize data from a config pokemon level move section
"""


def check_and_sanitize_moves(moves: list, pokemon_name: str) -> dict:
    """
    Split section into arrays ( forms ) , with top_comments,moves and bot_comments as a normalized
    reprensation of config pokemon level move section
    """
    template = None
    end = None
    form = None
    actual_form = None
    section = {
        'top_comments': [],
        'forms': OrderedDict(),
        'bot_comments': [],
    }
    if not re.search(r'(\[\[Septième génération]])|(\[\[Huitième génération]])|'
                     r'(Par montée en \[\[niveau]])|(Par \[\[CT]]\/\[\[CS]])|'
                     r'\{\{Jeu|SL}} et \{\{Jeu|USUL}}|(Par \[\[reproduction]])',
                     moves[0]):
        raise WrongHeaderError('Invalid header: {}'.format(moves[0]))
    section['top_comments'].append(moves[0])
    del moves[0]
    template_regex = r'.*{{#invoke:Apprentissage\|(niveau|capsule|disque|reproduction)\|.*'

    r = re.compile(template_regex)

    templates = len(list(filter(r.match, moves)))
    if templates == 0:
        raise TemplateNotFoundError('no pokemon move template found', {'wikitext': moves})

    forms = OrderedDict()
    if templates == 1:
        forms[pokemon_name] = {
            'top_comments': [],
            'moves': [],
            'bot_comments': [],
        }
        for move in moves:
            if not template and not re.match(template_regex, move) and not end:
                section['top_comments'].append(move)
            elif not template and re.match(template_regex, move):
                template = True
                end = False
            elif template and re.match(r'^}}$', move):
                template = False
                end = True
            elif end:
                section['bot_comments'].append(move)
            else:
                if 'moves' not in forms[pokemon_name]:
                    forms[pokemon_name]['moves'] = []
                forms[pokemon_name]['moves'].append(move)
        section['forms'] = forms
        return section

    for move in moves:
        if not template and not form and not bool(re.match(r'.*=.*=.*', move)) and not end:
            section['top_comments'].append(move)
        elif not template and form and bool(re.match(template_regex, move)):
            template = True
            end = False
        elif not template and bool(re.match(r'.*=.*=.*', move)):
            form = True
            end = False
            actual_form = move.strip().replace('=', '').strip()
            forms[actual_form] = {
                'top_comments': [],
                'moves': [],
                'bot_comments': [],
            }
        elif template and re.match(r'^}}$', move):
            template = False
            end = True
        elif template and form and not re.match(r'^}}$', move):
            forms[actual_form]['moves'].append(move)
        elif form and not re.match('.*=.*=.*', move) and not template and not end:
            forms[actual_form]['top_comments'].append(move)
        elif end:
            forms[actual_form]['bot_comments'].append(move)

    section['forms'] = forms

    return section
