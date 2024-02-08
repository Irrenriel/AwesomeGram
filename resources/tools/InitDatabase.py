# -*- coding: utf-8 -*-
import os
from importlib import import_module
from pathlib import Path
from string import punctuation
from sys import argv

from jinja2 import Environment, FileSystemLoader
from loguru import logger

from resources.base.core import DirectoriesAndFilesChecking
from resources.tools.core import CustomTool
from resources.tools.exceptions import DBConnectUrlNotFound, InvalidDatabaseName


class InitDatabase(CustomTool):
    __db_name = None

    def __init__(self, path: Path):
        super().__init__(path)

        if any([ch in self._db_name for ch in punctuation]):
            raise InvalidDatabaseName

        if len(self._db_name) > 64:
            raise InvalidDatabaseName

        self.db_connect = f'{self._db_name.upper()}_CONNECT'
        self.db_file = f"{self._db_name}.py"
        self.config = None

    def on_process(self):
        """
        Creating step by step structure:

        < ROOT >
            ⊳ core
                ⊳ database
                    ⊳ db.py
            ⊳ resources
                ⊳ models
                    ⊳ enums
                        ⊳ __init__.py
                        ⊳ languages.py
                    ⊳ tables
                        ⊳ __init__.py
                        ⊳ users.py

        """
        DirectoriesAndFilesChecking(
            [
                self.path / 'modules',
                self.path / 'resources',
                self.path / 'modules' / 'config.py'
            ]
        )

        self._check_config()

        async_mode = 'async_' if self.async_mode else ''
        template_path = self.path / "resources" / "tools" / "templates" / f"{async_mode}init_database_templates"

        self._creating_level(template_path, self.path)
        self._creating_files(template_path, self.path)

        logger.info(f'Successfully initiated database with "{self.db_file}" file!')

    @property
    def _db_name(self):
        if self.__db_name:
            return self.__db_name

        name_index = argv.index('--init-db') + 1

        if name_index >= len(argv) or '=' in argv[name_index]:
            self.__db_name = 'db'

        else:
            self.__db_name = argv[name_index].lower()

        return self.__db_name

    def _check_config(self):
        self.config = getattr(import_module('modules.config'), "config")

        if not hasattr(self.config, self.db_connect):
            raise DBConnectUrlNotFound(self.db_connect)

    @property
    def _data(self):
        return {
            'header': self.linux_header,
            'connect_name': self.db_connect
        }
