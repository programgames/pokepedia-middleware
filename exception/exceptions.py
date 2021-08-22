class UnrecoverableMessageHandlingError(Exception):

    def __init__(self, message):
        self.message = message


class InvalidResponse(Exception):

    def __init__(self, message):
        self.message = message
