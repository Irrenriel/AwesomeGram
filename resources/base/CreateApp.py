# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
from loguru import logger

from resources.base.core import ManageTool, DirectoriesAndFilesChecking


class CreateApp(ManageTool):
    def on_process(self):
        DirectoriesAndFilesChecking(
            [
                self.path / 'modules',
                self.path / 'modules' / 'handlers.py',
                self.path / 'modules' / 'middlewares.py',
                self.path / 'modules' / 'config.py'
            ]
        )

        template_path = self.path / "resources" / "base" / "templates" / "create_app_templates"

        tpl = Environment(loader=FileSystemLoader(template_path)).get_template('app.py-tpl')

        with open(self.path / 'app.py', mode='w', encoding='UTF-8') as f:
            f.write(tpl.render())

        logger.info('Successfully created "app.py" file!')
