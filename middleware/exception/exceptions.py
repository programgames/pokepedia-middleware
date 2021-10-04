from urllib.parse import unquote

class UnrecoverableMessageHandlingError(Exception):

    def __init__(self, message):
        self.message = message


class InvalidResponse(Exception):

    def __init__(self, message):
        self.message = message


class NotAvailableError(RuntimeError):

    def __init__(self, message):
        self.message = message


class SectionNotFoundException(NotAvailableError):
    additional_data = {
        'section_not_found': 'section',
        'generation': -1,
        'version_group': 'vg',
        'sections': {},
        'page': 'page'
    }

    def __init__(self, message, additional_data):
        self.message = message
        self.additional_data = additional_data

    def __str__(self):
        return f"Section not found / url : { unquote(self.additional_data['page'])} / section :" \
               f" {self.additional_data['section_not_found']}"


class DataFormatError(RuntimeError):
    def __init__(self, message):
        self.message = message


class WrongHeaderError(DataFormatError):
    def __init__(self, message):
        self.message = message


class TemplateNotFoundError(DataFormatError):
    def __init__(self, message):
        self.message = message


class SpecificCaseError(RuntimeError):
    additional_data = {}

    def __init__(self, message, additional_data):
        self.message = message
        self.additional_data = additional_data


class SpecificPokemonMoveError(SpecificCaseError):
    additional_data = {}

    def __init__(self, message, additional_data):
        self.message = message
        self.additional_data = additional_data


class SpecificPokemonMachineMoveError(SpecificPokemonMoveError):
    additional_data = {}

    def __init__(self, message, additional_data):
        self.message = message
        self.additional_data = additional_data
