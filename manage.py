import logging
from pathlib import Path
from sys import argv

from resources.base import *
from resources.utils._logging import GeneralLogger


def main():
    for i, arg in enumerate(argv):
        tool = {
            '--create-module': CreateModule,  # Creating New Module
            '--create-app': CreateApp,  # Creating Startup App
            '--help': Help,  # Help Menu
        }.get(arg)

        if tool is None:
            continue

        tool(Path(__file__).parent).on_process()
        break

    else:
        logging.warning("No available commands! Use 'python manage.py --help' to see commands!")


if __name__ == '__main__':
    GeneralLogger.register_logging('manage.log', debug=True)
    main()
