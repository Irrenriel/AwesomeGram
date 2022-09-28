from pathlib import Path
from sys import argv

from resources.utils.base.create_module import CreateModule


def main():
    for i, arg in enumerate(argv):
        tool = {
            '--create-module': CreateModule  # Creating New Module
        }.get(arg)

        if tool is None:
            continue

        tool(Path(__file__).parent).on_process()


if __name__ == '__main__':
    main()
