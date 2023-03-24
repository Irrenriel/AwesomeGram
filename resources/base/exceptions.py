# -*- coding: utf-8 -*-
__all__ = [
    'ModuleNameNotFound', 'InvalidModuleName', 'ModulesNotCreated'
]


class ManageError(Exception):
    """Base level exceptions raised when a manage.py errors."""


class ModuleNameNotFound(ManageError):
    def __init__(self):
        msg = 'Module name not passed.'
        super().__init__(msg)


class InvalidModuleName(ManageError):
    def __init__(self):
        msg = 'Invalid module name. Punctuation marks are not allowed and the maximum number of characters is 64.'
        super().__init__(msg)


class ModulesNotCreated(ManageError):
    def __init__(self, name: str):
        msg = f'Directory "{name}" not exist!' if '.' not in name else f'File "{name}" not exist!'
        msg += ' Please, create module with module creator. (manage.py --create-module <module_name>)'
        super().__init__(msg)

