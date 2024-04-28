from pathlib import Path
from sys import argv

try:
    from loguru import logger

except ModuleNotFoundError:
    install_requirements = r'''
.___                 __         .__  .__                               .__                                      __         ._.
|   | ____   _______/  |______  |  | |  |   _______   ____  ________ __|__|______   ____   _____   ____   _____/  |_  _____| |
|   |/    \ /  ___/\   __\__  \ |  | |  |   \_  __ \_/ __ \/ ____/  |  \  \_  __ \_/ __ \ /     \_/ __ \ /    \   __\/  ___/ |
|   |   |  \\___ \  |  |  / __ \|  |_|  |__  |  | \/\  ___< <_|  |  |  /  ||  | \/\  ___/|  Y Y  \  ___/|   |  \  |  \___ \ \|
|___|___|  /____  > |__| (____  /____/____/  |__|    \___  >__   |____/|__||__|    \___  >__|_|  /\___  >___|  /__| /____  >__
         \/     \/            \/                         \/   |__|                     \/      \/     \/     \/          \/ \/

'''
    print(f'{install_requirements}To install: pip install -r requirements.txt')
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
            '--init-db': InitDatabase,  # Initiating SQLAlchemy database connection
            '--create-model': CreateModel,  # Creating SQLAlchemy model

            # Other tools:
        }.get(arg)

        if tool is None:
            continue

        tool(Path(__file__).parent, i).on_process()
        break

    else:
        logger.warning("No available commands! Use 'python manage.py --help' to see commands!")


if __name__ == '__main__':
    # logger.add('/logs/manage.log')
    main()
