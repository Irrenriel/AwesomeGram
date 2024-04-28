# -*- coding: utf-8 -*-
__all__ = [
    'DBConnectUrlNotFound', 'InvalidDatabaseName', 'InvalidModelName'
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
