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
    additional_data = {}

    def __init__(self, message, additional_data):
        self.message = message
        self.additional_data = additional_data


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
