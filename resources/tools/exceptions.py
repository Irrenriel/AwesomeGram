# -*- coding: utf-8 -*-
__all__ = [

]


class ToolsError(Exception):
    """ Tools group level exceptions. """

class DBConnectUrlNotFound(ToolsError):
    def __init__(self, name: str):
        msg = f'There is no connection attribute "{name}" in the config!'
        super().__init__(msg)
