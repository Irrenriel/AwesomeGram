# -*- coding: utf-8 -*-
from loguru import logger


TXT = '''\
Available command to use:
    - python manage.py --create-module <module_name>   # Creating a new module rooting
    - python manage.py --create-app                    # Creating a new app.py file
    - python manage.py --help                          # Help menu with commands
    - python manage.py --init-db <db_engine_name>      # Initiating SQLAlchemy database connection
'''


class Help:
    def __init__(self, path):
        pass

    def on_process(self):
        logger.info(TXT)