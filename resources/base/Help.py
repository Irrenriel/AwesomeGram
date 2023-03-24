# -*- coding: utf-8 -*-
import logging


TXT = '''\
Available command to use:
    - python manage.py --create-module <module_name>   # Creating a new module rooting
    - python manage.py --create-app                    # Creating a new app.py file
    - python manage.py --help                          # Help menu with commands
'''


class Help:
    def __init__(self, path):
        pass

    def on_process(self):
        logging.info(TXT)