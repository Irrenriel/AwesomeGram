# -*- coding: utf-8 -*-
__all__ = [
    'DBConnectUrlNotFound', 'InvalidDatabaseName', 'InvalidModelName', 'UnknownColumnType',
    'UnknownColumnOption', 'ModelAlreadyExists'
]


class ToolsError(Exception):
    """ Tools group level exceptions. """


class DBConnectUrlNotFound(ToolsError):
    def __init__(self, name: str):
        msg = f'There is no connection attribute "{name}" in the config!'
        super().__init__(msg)


class InvalidDatabaseName(ToolsError):
    def __init__(self):
        msg = 'Invalid database name. Punctuation marks are not allowed and the maximum number of characters is 64.'
        super().__init__(msg)


class InvalidModelName(ToolsError):
    def __init__(self):
        msg = 'Invalid model name. Punctuation marks are not allowed and the maximum number of characters is 64.'
        super().__init__(msg)


class UnknownColumnType(ToolsError):
    def __init__(self, name: str, available: list):
        msg = f'Unknown column type "{name}". Available types: {", ".join(available)}.'
        super().__init__(msg)


class UnknownColumnOption(ToolsError):
    def __init__(self, name: str, available: list):
        msg = f'Unknown column type or option "{name}". Available options: {", ".join(available)}.'
        super().__init__(msg)


class ModelAlreadyExists(ToolsError):
    def __init__(self, path: str):
        msg = f'Model file "{path}" already exists! Pass overwrite=true to replace it.'
        super().__init__(msg)
