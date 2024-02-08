# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
from loguru import logger

from resources.base.core import ManageTool, DirectoriesAndFilesChecking


class CreateApp(ManageTool):
    def on_process(self):
        DirectoriesAndFilesChecking(
            [
                self.path / 'modules',
                self.path / 'modules' / 'config.py',
                self.path / 'modules' / 'installing.py'
            ]
        )

        template_path = self.path / "resources" / "base" / "templates" / "create_app_templates"

        tpl = Environment(loader=FileSystemLoader(template_path)).get_template('app.py-tpl')

        with open(self.path / 'app.py', mode='w', encoding='UTF-8') as f:
            text = tpl.render()
            f.write(text + ('' if text.endswith('\n') else '\n'))

        logger.info('Successfully created "app.py" file!')
