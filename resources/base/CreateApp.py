# -*- coding: utf-8 -*-
import os

from jinja2 import Environment, FileSystemLoader
from loguru import logger

from resources.base.exceptions import ModulesNotCreated


class CreateApp:
    def __init__(self, path):
        self.path = path
        self.template_path = self.path / "resources" / "base" / "templates" / "create_app_templates"

    def on_process(self):
        self._check_leveling()

        tpl = Environment(loader=FileSystemLoader(self.template_path)).get_template('app.py-tpl')

        with open(self.path / 'app.py', mode='w', encoding='UTF-8') as f:
            f.write(tpl.render())

        logger.info('Successfully created "app.py" file!')

    def _check_leveling(self):
        levels_and_files = [
            'modules',
            'modules\\handlers.py',
            'modules\\middlewares.py',
            'modules\\config.py',
        ]

        for level_or_file in levels_and_files:
            foo = os.path.isfile if '.' in level_or_file else os.path.exists

            if not foo(self.path / level_or_file):
                raise ModulesNotCreated(level_or_file)
