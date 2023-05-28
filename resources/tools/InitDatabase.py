# -*- coding: utf-8 -*-
import os
from importlib import import_module
from pathlib import WindowsPath
from string import punctuation
from sys import argv

from jinja2 import Environment, FileSystemLoader
from loguru import logger

from resources.base.core import ManageTool, DirectoriesAndFilesChecking
from resources.tools.exceptions import DBConnectUrlNotFound, InvalidDatabaseName


class InitDatabase(ManageTool):
    def __init__(self, path: WindowsPath):
        name_index = argv.index('--init-db') + 1
        super().__init__(path)

        self.db_name = 'db' if name_index >= len(argv) else argv[name_index].lower()

        if any([ch in self.db_name for ch in punctuation]):
            raise InvalidDatabaseName

        if len(self.db_name) > 64:
            raise InvalidDatabaseName

        self.db_connect = f'{self.db_name.upper()}_CONNECT'
        self.db_file = f"{self.db_name}.py"

    def on_process(self):
        DirectoriesAndFilesChecking(
            [
                self.path / 'modules',
                self.path / 'modules' / 'handlers.py',
                self.path / 'modules' / 'middlewares.py',
                self.path / 'modules' / 'config.py'
            ]
        )

        core_path = self.path / "core"
        database_core_path = core_path / "database"
        template_path = self.path / "resources" / "tools" / "templates" / "init_database_templates"

        config = getattr(import_module('modules.config'), "config")

        if not hasattr(config, self.db_connect):
            raise DBConnectUrlNotFound(self.db_connect)

        file = os.path.isfile(database_core_path / self.db_file)

        if not file or (file and self.overwrite):
            if not os.path.exists(core_path):
                os.mkdir(core_path)
                logger.info('Successfully created "core" folder!')

            if not os.path.exists(database_core_path):
                os.mkdir(database_core_path)
                logger.info('Successfully created "core/database" folder!')

            tpl = Environment(loader=FileSystemLoader(template_path)).get_template('db.py-tpl')

            with open(database_core_path / self.db_file, mode='w', encoding='UTF-8') as f:
                f.write(tpl.render(**self.data))

            if file:
                logger.info(f'Successfully initiated database with overwrite "{self.db_file}" file!')

            else:
                logger.info(f'Successfully initiated database with "{self.db_file}" file!')

        else:
            logger.info(f'Failed initiating database with "{self.db_file}" file! Already exist!')

    @property
    def data(self):
        return {
            'header': self.linux_header,
            'connect_name': self.db_connect
        }
