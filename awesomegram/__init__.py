# -*- coding: utf-8 -*-
import argparse as _argparse
import os as _os
from importlib.metadata import version as _version
from pathlib import Path

from .tools import *

try:
    VERSION = _version("AwesomeGram")
except Exception:
    VERSION = "ERROR"


class ConsoleCommandParser:
    def __init__(self):
        self.path = _os.getcwd()
        self.lib_path = Path(__file__).parent

        self.parser = _argparse.ArgumentParser(
            description="AwesomeGram commands information"
        )

        self.parser.add_argument(
            "-v", "--version",
            action="version",
            version=f"AwesomeGram {VERSION}",
            help="Show the version and exit"
        )

        subparsers = self.parser.add_subparsers(dest="command", help="Available commands")

        # Command `start-project`:
        start_parser = subparsers.add_parser(
            "start-project",
            help="Start a new project"
        )
        start_parser.add_argument(
            "name",
            help="Project name",
            type=StartProject.project_name_check
        )

    def __call__(self):
        args: _argparse.Namespace = self.parser.parse_args()

        match args.command:  # noqa
            case 'start-project':
                tool = StartProject(path=self.path, lib_path=self.lib_path, args=args, version=VERSION)

            case _:
                return self.parser.print_help()

        return tool()


main = ConsoleCommandParser()
