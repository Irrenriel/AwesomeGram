# -*- coding: utf-8 -*-
from os import path
from pathlib import WindowsPath
from typing import List

from resources.base.exceptions import ModulesNotCreated


class DirectoriesAndFilesChecking:
    def __new__(cls, directories_and_files: List[WindowsPath], *args, **kwargs):
        for directory_or_file in directories_and_files:
            str_directory_or_file = str(directory_or_file)
            if not (path.isfile if '.' in str_directory_or_file else path.exists)(directory_or_file):
                raise ModulesNotCreated(str_directory_or_file)
