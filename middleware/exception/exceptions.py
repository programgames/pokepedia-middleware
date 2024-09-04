from urllib.parse import unquote
from requests import HTTPError

class UnrecoverableMessageHandlingException(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidResponse(HTTPError):
    def __init__(self, message):
        super().__init__(message)

class MissingOptionException(RuntimeError):
    def __init__(self, message):
        super().__init__(message)

class NotAvailableError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)

class SectionNotFoundException(NotAvailableError):
    def __init__(self, message, additional_data):
        super().__init__(message)
        self.additional_data = additional_data

    def __str__(self):
        return (f"Section not found / URL: {unquote(self.additional_data.get('page', ''))} / "
                f"Section: {self.additional_data.get('section_not_found', '')}")

class DataFormatError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)

class WrongHeaderError(DataFormatError):
    def __init__(self, message):
        super().__init__(message)

class TemplateNotFoundError(DataFormatError):
    def __init__(self, message, additional_data=None):
        super().__init__(message)
        self.additional_data = additional_data or {}

class PokemonMoveException(RuntimeError):
    def __init__(self, message, additional_data=None):
        super().__init__(message)
        self.additional_data = additional_data or {}

class NoMachineMoveLearnAndNoTemplateException(PokemonMoveException):
    def __init__(self, message, additional_data=None):
        super().__init__(message, additional_data)

class NoEggMoveLearnAndNoTemplateException(PokemonMoveException):
    def __init__(self, message, additional_data=None):
        super().__init__(message, additional_data)

class MissingEggMoveTemplateException(PokemonMoveException):
    def __init__(self, message, additional_data=None):
        super().__init__(message, additional_data)

class MissingMachineMoveTemplateException(PokemonMoveException):
    def __init__(self, message, additional_data=None):
        super().__init__(message, additional_data)

class UnsupportedException(RuntimeError):
    def __init__(self, message):
        super().__init__(message)

class InvalidConditionException(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
