# -*- coding: utf-8 -*-
from pathlib import Path

from loguru import logger

from resources.base.core import AbstractTool

TXT = '''
Available commands to use:
    > python manage.py --create-module <module_name> [overwrite=true/false, linux=true/false]   # Creating a new module root
    > python manage.py --create-app [overwrite=true/false, linux=true/false]                    # Creating a new app.py file
    > python manage.py --init-db <db_engine_name>                                               # Initiating SQLAlchemy database connection
    > python manage.py --help                                                                   # Help menu with commands
'''


class Help(AbstractTool):
    def __init__(self, path: Path):
        pass

    def on_process(self):
        logger.info(TXT)
