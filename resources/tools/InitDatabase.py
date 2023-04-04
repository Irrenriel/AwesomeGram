import os
from importlib import import_module
from sys import argv

from jinja2 import Environment, FileSystemLoader
from loguru import logger

from resources.base.exceptions import ModulesNotCreated
from resources.tools.exceptions import DBConnectUrlNotFound


class InitDatabase:
    def __init__(self, path):
        index = argv.index('--init-db')
        name_index = index + 1

        # Default values before args processing:
        self.overwrite = True
        self.linux_mode = True
        self.linux_header = f'# -*- coding: utf-8 -*-\n' if self.linux_mode else ''

        self._args_processing(name_index)

        self.db_name = 'db' if name_index >= len(argv) else argv[name_index].lower()
        self.db_connect = f'{self.db_name.upper()}_CONNECT'
        self.db_file = f"{self.db_name}.py"

        self.path = path
        self.core_path = self.path / "core"
        self.template_path = self.path / "resources" / "tools" / "templates" / "init_database_templates"

    def on_process(self):
        self._check_leveling()

        config = getattr(import_module('modules.config'), "config")

        if not hasattr(config, self.db_connect):
            raise DBConnectUrlNotFound(self.db_connect)

        file = os.path.isfile(self.core_path / self.db_file)

        if not file or (file and self.overwrite):
            if not os.path.exists(self.core_path):
                os.mkdir(self.core_path)
                logger.info('Successfully created "core" folder!')

            tpl = Environment(loader=FileSystemLoader(self.template_path)).get_template('db.py-tpl')

            with open(self.core_path / self.db_file, mode='w', encoding='UTF-8') as f:
                f.write(tpl.render(**self.data))

            if file:
                logger.info(f'Successfully initiated database with overwrite "{self.db_file}" file!')

            else:
                logger.info(f'Successfully initiated database with "{self.db_file}" file!')

        else:
            logger.info(f'Failed initiating database with "{self.db_file}" file! Already exist!')

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

    @property
    def data(self):
        return {
            'header': self.linux_header,
            'connect_name': self.db_connect
        }
