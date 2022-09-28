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
    def __init__(self, msg: str):
        super().__init__(msg)

