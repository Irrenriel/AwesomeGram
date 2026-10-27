# -*- coding: utf-8 -*-
from os import path
from pathlib import Path
from typing import List

from resources.base.exceptions import ModulesNotCreated


class DirectoriesAndFilesChecking:
    def __new__(cls, directories_and_files: List[Path], *args, **kwargs):
        for directory_or_file in directories_and_files:
            # File or directory is decided by the last part only: "my.bot/modules" is a directory
            is_file = bool(Path(directory_or_file).suffix)
            if not (path.isfile if is_file else path.exists)(directory_or_file):
                raise ModulesNotCreated(str(directory_or_file))
