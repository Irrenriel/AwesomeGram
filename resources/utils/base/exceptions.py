__all__ = [
    'ModuleNameNotFound', 'InvalidModuleName'
]


class ManageError(Exception):
    """Base level exceptions raised when a manage.py errors."""

    pass


class ModuleNameNotFound(ManageError):
    def __init__(self):
        msg = 'Module name not passed.'
        super().__init__(msg)


class InvalidModuleName(ManageError):
    def __init__(self):
        msg = 'Invalid module name. Punctuation marks are not allowed.'
        super().__init__(msg)

