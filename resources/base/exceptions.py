# -*- coding: utf-8 -*-
__all__ = [
    'ModuleNameNotFound', 'InvalidModuleName', 'ModulesNotCreated', 'LangNotFound'
]


class BaseError(Exception):
    """ Base level exceptions raised when a manage.py errors. """


class ModuleNameNotFound(BaseError):
    def __init__(self):
        msg = 'Module name not passed.'
        super().__init__(msg)


class InvalidModuleName(BaseError):
    def __init__(self):
        msg = 'Invalid module name. Punctuation marks are not allowed and the maximum number of characters is 64.'
        super().__init__(msg)


class ModulesNotCreated(BaseError):
    def __init__(self, name: str):
        msg = f'Directory "{name}" not exist!' if '.' not in name else f'File "{name}" not exist!'
        msg += ' Please, create module with module creator. (manage.py --create-module <module_name>)'
        super().__init__(msg)

class LangNotFound(BaseError):
    """ Lang not found """
