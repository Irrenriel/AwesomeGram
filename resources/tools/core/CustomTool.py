# -*- coding: utf-8 -*-
import os
from abc import ABC
from pathlib import Path
from sys import argv
from typing import Optional

from jinja2 import Environment, FileSystemLoader

from resources.base.core import AbstractTool
from resources.base.exceptions import ArgumentValueNotFound


class CustomTool(AbstractTool, ABC):
    overwrite = True
    linux_mode = True
    async_mode = False
    linux_header = f'# -*- coding: utf-8 -*-\n'

    def __init__(self, path: Path, name_index: Optional[int] = None):
        self.path = path

        if name_index and name_index >= len(argv):
            raise ArgumentValueNotFound(argv[name_index])

        self._args_processing(name_index or 0)

    def _args_processing(self, index):
        arg_keys = ('overwrite', 'linux', 'async')

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

            # Async Mode:
            if k == 'async':
                if v not in ['true', 'false', '1', '0']:
                    continue

                self.async_mode = True if v in ['true', '1'] else False

            self.linux_header = f'# -*- coding: utf-8 -*-\n' if self.linux_mode else ''

    def _creating_level(self, tpl_path, src_path):
        for ent in os.listdir(tpl_path):
            clean = self._clear_name(ent)

            if not clean or '.' in ent:
                continue

            if not os.path.exists(src_path / clean):
                os.makedirs(src_path / clean)

            self._creating_level(tpl_path / ent, src_path / clean)

    def _creating_files(self, tpl_path, src_path):
        for ent in os.listdir(tpl_path):
            clean = self._clear_name(ent)

            if not clean:
                continue

            # Python files:
            if clean.endswith('.py') or clean.endswith('.yml'):
                if os.path.isfile(src_path / clean) and not self.overwrite:
                    continue

                tpl = Environment(loader=FileSystemLoader(tpl_path)).get_template(ent)

                with open(src_path / clean, mode='w', encoding='UTF-8') as f:
                    text = tpl.render(**self._data)
                    f.write(text + ('' if text.endswith('\n') else '\n'))

            elif '.' in ent:
                continue

            else:
                self._creating_files(tpl_path / ent, src_path / clean)

    @staticmethod
    def _clear_name(ent):
        if not ent.endswith('-tpl'):
            return

        return ent.replace('-tpl', '')

    @property
    def _data(self):
        return {}
