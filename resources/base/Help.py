# -*- coding: utf-8 -*-
from pathlib import Path

from loguru import logger

from resources.base.core import AbstractTool

TXT = '''
Available commands to use:
    > python manage.py --create-module <module_name> [overwrite=true/false, linux=true/false]   # Creating a new module root (existing files are kept unless overwrite=true)
    > python manage.py --create-app [overwrite=true/false, linux=true/false]                    # Creating a new app.py file
    > python manage.py --init-db <db_engine_name> [async=true/false, overwrite=true/false]       # Initiating SQLAlchemy database connection
    > python manage.py --create-model <model_name> <field>[:type][:option] ...                  # Creating SQLAlchemy model (e.g. id:int:primary)
    > python manage.py --help                                                                   # Help menu with commands
'''


class Help(AbstractTool):
    def __init__(self, path: Path, *args, **kwargs):
        pass

    def on_process(self):
        logger.info(TXT)
