# -*- coding: utf-8 -*-
from abc import ABC
from pathlib import WindowsPath
from sys import argv
from typing import Optional

from resources.base.core.AbstractTool import AbstractTool
from resources.base.exceptions import ModuleNameNotFound


class ManageTool(AbstractTool, ABC):
    overwrite = True
    linux_mode = True
    linux_header = f'# -*- coding: utf-8 -*-\n'

    def __init__(self, path: WindowsPath, name_index: Optional[int] = None):
        self.path = path

        if name_index is None:
            return

        if name_index >= len(argv):
            raise ModuleNameNotFound

        self._args_processing(name_index)

    def _args_processing(self, index):
        arg_keys = ('overwrite', 'linux',)

        for arg in argv[index:]:
            if '=' not in arg:
                continue

            args = arg.split('=')

            if len(args) != 2:
                continue

            k, v = [i.lower() for i in args]

            if k not in arg_keys:
                continue

            # Overwriting:
            if k == 'overwrite':
                if v not in ['true', 'false', '1', '0']:
                    continue

                self.overwrite = True if v in ['true', '1'] else False

            # Linux Encoding:
            if k == 'linux':
                if v not in ['true', 'false', '1', '0']:
                    continue

                self.linux_mode = True if v in ['true', '1'] else False

            self.linux_header = f'# -*- coding: utf-8 -*-\n' if self.linux_mode else ''
