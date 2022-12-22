import re
from collections import OrderedDict
from middleware.exception import WrongHeaderError, TemplateNotFoundError
from middleware.util.helper.pokemonhelper import get_default_pokemon_form_name_from_database

"""
Parse, check, and sanitize data from a config Pokémon level move section.
"""


def check_and_sanitize_moves(moves: list, pokemon_name: str) -> dict:
    """
    Split section into arrays (forms), with top_comments, moves, and bot_comments
    as a normalized representation of config Pokémon level move section.
    """
    section = {
        'top_comments': [],
        'forms': OrderedDict(),
        'bot_comments': [],
    }

    # Validate header
    header_pattern = (
        r'(\[\[Huitième génération]])|(\[\[Neuvième génération]])'
        r'(Par montée en \[\[niveau]])|(Par \[\[CT]]\/\[\[CS]])|(Par \[\[CT]])||(Par \[\[DT]])'
        r'\{\{Jeu\|SL}} et \{\{Jeu\|USUL}}|(Par \[\[reproduction]])'
    )
    if not re.search(header_pattern, moves[0]):
        raise WrongHeaderError(f'Invalid header: {moves[0]}')

    section['top_comments'].append(moves.pop(0))  # Remove and store the header

    # Template regex
    template_regex = r'.*{{#invoke:Apprentissage\|(niveau|capsule|disque|reproduction)\|.*'
    template_matcher = re.compile(template_regex)

    templates = len(list(filter(template_matcher.match, moves)))
    if templates == 0:
        raise TemplateNotFoundError('No Pokémon move template found', {'wikitext': moves})

    forms = OrderedDict()

    pokemon_name = get_default_pokemon_form_name_from_database(pokemon_name)
    if templates == 1:
        forms[pokemon_name] = {
            'top_comments': [],
            'moves': [],
            'bot_comments': [],
        }
        _process_single_template(moves, section, forms[pokemon_name])
        section['forms'] = forms
        return section

    _process_multiple_templates(moves, section, forms)

    section['forms'] = forms
    return section


def _process_single_template(moves: list, section: dict, form: dict):
    """
    Process a single form/template and populate the section with comments and moves.
    """
    in_template = False
    in_end_section = False

    for move in moves:
        if not in_template and not re.match(r'^}}$', move) and not in_end_section and not re.match(r'.*{{#invoke:Apprentissage\|.*', move):
            section['top_comments'].append(move)
        elif re.match(r'^}}$', move):
            in_template = False
            in_end_section = True
            # section['bot_comments'].append(move)
        elif re.match(r'.*{{#invoke:Apprentissage\|.*', move) :
            in_template = True
            in_end_section = False
        elif in_end_section:
            section['bot_comments'].append(move)
        else:
            form['moves'].append(move)


def _process_multiple_templates(moves: list, section: dict, forms: OrderedDict):
    """
    Process multiple forms/templates and populate the section with comments and moves.
    """
    in_template = False
    in_form = False
    in_end_section = False
    current_form = None

    for move in moves:
        if not in_template and not in_form and not re.match(r'.*=.*=.*', move) and not in_end_section:
            section['top_comments'].append(move)
        elif re.match(r'.*=.*=.*', move) and not re.match(r'.*{{#invoke:Apprentissage\|.*', move) :
            in_form = True
            in_template = False
            in_end_section = False
            current_form = move.strip().replace('=', '').strip()
            forms[current_form] = {
                'top_comments': [],
                'moves': [],
                'bot_comments': [],
            }
        elif in_form and re.match(r'.*{{#invoke:Apprentissage\|.*', move):
            in_template = True
            in_end_section = False
        elif in_template and re.match(r'^}}$', move):
            in_template = False
            in_end_section = True
        elif in_template and not re.match(r'^}}$', move):
            forms[current_form]['moves'].append(move)
        elif in_form and not re.match(r'.*=.*=.*', move) and not in_template and not in_end_section:
            forms[current_form]['top_comments'].append(move)
        elif in_end_section:
            forms[current_form]['bot_comments'].append(move)
