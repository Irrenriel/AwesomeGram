# -*- coding: utf-8 -*-
import os
from pathlib import Path
from string import punctuation
from sys import argv

from loguru import logger

from resources.base.core import ManageTool
from resources.base.exceptions import InvalidModuleName


class CreateModule(ManageTool):
    template_module_name = 'module_name'

    def __init__(self, path: Path):
        name_index = argv.index('--create-module') + 1
        super().__init__(path, name_index)

        self.name = argv[name_index].lower()

        if any([ch in self.name for ch in punctuation]):
            raise InvalidModuleName

        if len(self.name) > 64:
            raise InvalidModuleName

    def on_process(self):
        """
        Creating step by step structure:

        < ROOT >
            ⊳ modules
                ⊳ config.py
                ⊳ installing.py (Handlers & Middlewares from all modules are imported here)
                ⊳ states.py (States from all modules are imported here)
                ⊳ < module name >
                    ⊳ functions
                        ⊳ __init__.py
                        ⊳ < module name >.py
                    ⊳ handlers.py
                    ⊳ keyboards.py
                    ⊳ states.py
            ⊳ resources
                ⊳ locales
                    ⊳ en.yml
                ⊳ middlewares
                    ⊳ __init__.py
                    ⊳ main_middleware.py
                    ⊳ throttle_middleware.py

        """
        # Paths
        template_path = self.path / "resources" / "base" / "templates" / "create_module_templates"

        self._creating_level(template_path, self.path)
        self._creating_files(template_path, self.path)

        logger.info(f'Successfully created module "{self.name}"!')

    def _clear_name(self, ent: str):
        if not ent.endswith('-tpl'):
            return

        clean = ent.replace('-tpl', '')

        if not self.template_module_name:
            return clean

        if clean.startswith(self.template_module_name):
            clean = clean.replace(self.template_module_name, self.name)

        return clean

    @property
    def _data(self):
        return {
            'header': self.linux_header,
            'name': self.name,
            'modules': [i for i in os.listdir(self.path / "modules") if '.' not in i and i != 'middlewares']
        }
