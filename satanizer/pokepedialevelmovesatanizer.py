import re

from exception import WrongHeaderError


class PokepediaLevelMoveSatanizer:
    def __init__(self):
        pass

    def check_and_sanitize_moves(self, moves: list) -> dict:
        template = None
        end = None
        form = None
        actual_form = None
        section = {
            'topComments': [],
            'forms': [],
            'botComments': [],
        }
        if moves[0] not in [
            '=== Par montée en [[niveau]] ===',
            '==== Par montée en niveau ====',
            '===Par montée en [[niveau]] ===',
            '==== [[Septième génération]] ====',
            '==== [[Huitième génération]] ====',
        ]:
            raise WrongHeaderError('nvalid header: {}'.format(moves[0]))
        section['topComments'].append(moves[0])
        del moves[0]
        r = re.compile(r'{{#invoke:Apprentissage\|niveau\|')

        templates = len(list(filter(r.match, moves)))
        if templates == 0:
            raise RuntimeError('no level template found')

        forms = {}
        if templates == 1:
            forms['uniqForm'] = {
                'topComments': [],
                'forms': [],
                'botComments': [],
            }
            for key, move in moves:
                if not template and not re.match(r'{{#invoke:Apprentissage\|niveau\|', move):
                    section['topComments'].append(move)
                elif not template and re.match(r'{{#invoke:Apprentissage\|niveau\|', move):
                    template = True
                elif template and re.match(r'}}', move):
                    template = False
                    end = True
                elif end:
                    section['botComments'].append(move)
                else:
                    forms['uniqForm']['moves'].append([])
            section['forms'] = forms
            return section

        for key, move in moves:
            if template and not form and not re.match(r'=.*=', move):
                section['topComments'].append(move)
            elif not template and form and re.match(r'{{#invoke:Apprentissage\|niveau\|', move):
                template = True
            elif not template and re.match(r'=.*=', move):
                form = True
                end = False
                actual_form = move.strip().replace('=', '').strip()
            elif template and re.match(r'}}', move):
                template = False
                end = True
            elif template and form and not re.match(r'}}', move):
                forms[actual_form]['moves'].append(move)
            elif form and not re.match('=.*=', move) and not template:
                forms[actual_form]['topComments'].append(move)
            elif form and not template and re.match(r'=.*=', move):
                form = True
                actual_form = move.strip().replace('=', '')
                forms[actual_form] = {
                    'topComments': [],
                    'moves': [],
                    'botComments': [],
                }
            elif end:
                forms[actual_form]['botComments'].append(move)

        section['forms'] = forms

        return section
