class UnrecoverableMessageHandlingError(Exception):

    def __init__(self, message):
        self.message = message


class InvalidResponse(Exception):

    def __init__(self, message):
        self.message = message


class NotAvailableError(RuntimeError):

    def __init__(self, message):
        self.message = message


class DataFormatError(RuntimeError):
    def __init__(self, message):
        self.message = message


class WrongHeaderError(DataFormatError):
    def __init__(self, message):
        self.message = message


class TemplateNotFound(DataFormatError):
    def __init__(self, message):
        self.message = message
