# -*- coding: utf-8 -*-
import os
from string import punctuation
from sys import argv

from jinja2 import Environment, FileSystemLoader
from loguru import logger

from resources.base.exceptions import ModuleNameNotFound, InvalidModuleName


class CreateModule:
    def __init__(self, path):
        index = argv.index('--create-module')
        name_index = index + 1

        if name_index >= len(argv):
            raise ModuleNameNotFound

        self.name = argv[name_index].lower()

        if any([ch in self.name for ch in punctuation]):
            raise InvalidModuleName

        if len(self.name) > 64:
            raise InvalidModuleName

        # Default values before args processing:
        self.overwrite = True
        self.linux_mode = True
        self.linux_header = f'# -*- coding: utf-8 -*-\n' if self.linux_mode else ''

        self._args_processing(name_index)

        self.path = path
        self.template_path = self.path / "resources" / "base" / "templates" / "create_module_templates"
        self.template_module_name = 'module_name'

        self.modules_path = self.path / "modules"

    def on_process(self):
        """
        Creating step by step structure:

        < ROOT >
            ⊳ modules
                ⊳ handlers.py (Handlers from all modules are imported here)
                ⊳ states.py (States from all modules are imported here)
                ⊳ < module name >
                    ⊳ functions
                        ⊳ __init__.py
                        ⊳ < module name >.py
                    ⊳ config.py
                    ⊳ handlers.py
                    ⊳ middlewares.py
                    ⊳ states.py
            ⊳ resources
                ⊳ locales
                ⊳ middlewares
                    ⊳ __init__.py
                    ⊳ main_middleware.py
                    ⊳ throttle_middleware.py

        """
        self._creating_level(self.template_path, self.path)
        self._creating_files(self.template_path, self.path)

        logger.info(f'Successfully created module "{self.name}"!')

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
                    f.write(tpl.render(**self.data))

            elif '.' in ent:
                continue

            else:
                self._creating_files(tpl_path / ent, src_path / clean)

    def _clear_name(self, ent):
        if not ent.endswith('-tpl'):
            return

        clean = ent.replace('-tpl', '')

        if clean.startswith(self.template_module_name):
            clean = clean.replace(self.template_module_name, self.name)

        return clean

    def _args_processing(self, index):
        arg_keys = [
            'overwrite', 'linux'
        ]

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

    @property
    def data(self):
        return {
            'header': self.linux_header,
            'name': self.name,
            'modules': [i for i in os.listdir(self.modules_path) if '.' not in i and i != 'middlewares']
        }
