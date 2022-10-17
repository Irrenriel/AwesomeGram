from pathlib import Path
from sys import argv

from resources.utils.base.create_app import CreateApp
from resources.utils.base.create_module import CreateModule
from resources.utils.logging import GeneralLogger


def main():
    for i, arg in enumerate(argv):
        tool = {
            '--create-module': CreateModule,  # Creating New Module
            '--create-app': CreateApp,  # Creating Startup App
        }.get(arg)

        if tool is None:
            continue

        tool(Path(__file__).parent).on_process()
        break


if __name__ == '__main__':
    GeneralLogger.register_logging('manage.log', debug=True)
    main()
