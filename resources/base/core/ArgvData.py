# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class ArgvData:
    command: str
    argv: tuple[str]
    content: tuple[str]
