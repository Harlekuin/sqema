"""Define Execptions."""


class NotAValidDefinitionError(Exception):
    def __init__(self):
        self.msg = "Unknown Definition Type"
