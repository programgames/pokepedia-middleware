from urllib.parse import unquote

from requests import HTTPError


class UnrecoverableMessageHandlingException(Exception):

    def __init__(self, message):
        self.message = message


class InvalidResponse(HTTPError):

    def __init__(self, message):
        self.message = message


class MissingOptionException(RuntimeError):
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
        return f"Section not found / url : {unquote(self.additional_data['page'])} / section :" \
               f" {self.additional_data['section_not_found']}"


class DataFormatError(RuntimeError):
    def __init__(self, message):
        self.message = message


class WrongHeaderError(DataFormatError):
    def __init__(self, message):
        self.message = message


class TemplateNotFoundError(DataFormatError):
    additional_data = {}

    def __init__(self, message, additional_data):
        self.message = message
        self.additional_data = additional_data


class PokemonMoveException(RuntimeError):
    additional_data = {}

    def __init__(self, message, additional_data):
        self.message = message
        self.additional_data = additional_data


class NoMachineMoveLearnAndNoTemplateException(PokemonMoveException):
    additional_data = {}

    def __init__(self, message, additional_data):
        self.message = message
        self.additional_data = additional_data


class NoEggMoveLearnAndNoTemplateException(PokemonMoveException):
    additional_data = {}

    def __init__(self, message, additional_data):
        self.message = message
        self.additional_data = additional_data


class MissingEggMoveTemplateException(PokemonMoveException):
    additional_data = {}

    def __init__(self, message, additional_data):
        self.message = message
        self.additional_data = additional_data


class MissingMachineMoveTemplateException(PokemonMoveException):
    additional_data = {}

    def __init__(self, message, additional_data):
        self.message = message
        self.additional_data = additional_data


class UnsupportedException(RuntimeError):
    def __init__(self, message):
        self.message = message


class InvalidConditionException(RuntimeError):
    def __init__(self, message):
        self.message = message
