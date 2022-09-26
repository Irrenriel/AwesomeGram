from pathlib import Path
from string import punctuation
from sys import argv

from resources.utils.base.create_module import CreateModule
from resources.utils.base.exceptions import ModuleNameNotFound, InvalidModuleName


# Settings:

"""Creating a module for Linux if True. Header added: LINUX_HEADER"""
LINUX_ENCODE = False
LINUX_HEADER = '# -*- coding: utf-8 -*-'


# Constant variables:

PRE_COMMANDS = [
    '--create-module'
]

MAX_LENGTH = 64


def main():
    for i, arg in enumerate(argv):
        tool = None

        # Creating New Module:
        if '--create-module' in arg:
            if i + 1 >= len(argv) or argv[i + 1] in PRE_COMMANDS:
                raise ModuleNameNotFound

            name = argv[i + 1].lower()

            if any([ch in name for ch in punctuation]) or len(name) > MAX_LENGTH:
                raise InvalidModuleName

            tool = CreateModule(Path(__file__).parent, name, LINUX_ENCODE, LINUX_HEADER)

        if tool is None:
            continue

        tool.on_process()


if __name__ == '__main__':
    main()
