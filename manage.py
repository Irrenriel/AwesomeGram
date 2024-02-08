from pathlib import Path
from sys import argv

try:
    from loguru import logger

except ModuleNotFoundError:
    print("Please install requirements!")
    exit()

from resources.base import *
from resources.tools import *


def main():
    for i, arg in enumerate(argv):
        tool = {
            # Base:
            '--help': Help,  # Help Menu
            '--create-module': CreateModule,  # Creating New Module
            '--create-app': CreateApp,  # Creating Startup App

            # Tools:
            '--init-db': InitDatabase  # Initiating SQLAlchemy database connection

            # Other tools:
        }.get(arg)

        if tool is None:
            continue

        tool(Path(__file__).parent).on_process()
        break

    else:
        logger.warning("No available commands! Use 'python manage.py --help' to see commands!")


if __name__ == '__main__':
    # logger.add('/logs/manage.log')
    main()
