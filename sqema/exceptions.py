"""Define Execptions."""


class NotAValidDefinitionError(Exception):
    def __init__(self, cm):
        self.msg = "Unknown Definition Type"
