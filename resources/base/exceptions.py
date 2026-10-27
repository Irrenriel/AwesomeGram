# -*- coding: utf-8 -*-
from pathlib import Path

__all__ = [
    'ArgumentValueNotFound', 'InvalidModuleName', 'ModulesNotCreated', 'LangNotFound'
]


class BaseError(Exception):
    """ Base level exceptions raised when a manage.py errors. """


class ArgumentValueNotFound(BaseError):
    def __init__(self, arg: str):
        msg = f'Argument "{arg}" must be passed a value!'
        super().__init__(msg)


class InvalidModuleName(BaseError):
    def __init__(self):
        msg = 'Invalid module name. Punctuation marks are not allowed and the maximum number of characters is 64.'
        super().__init__(msg)


class ModulesNotCreated(BaseError):
    def __init__(self, name: str):
        msg = f'File "{name}" not exist!' if Path(name).suffix else f'Directory "{name}" not exist!'
        msg += ' Please, create module with module creator. (manage.py --create-module <module_name>)'
        super().__init__(msg)


class LangNotFound(BaseError):
    """ Lang not found """
