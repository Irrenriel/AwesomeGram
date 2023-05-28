# -*- coding: utf-8 -*-
from abc import ABC

from resources.base.core import AbstractTool


class CustomTool(AbstractTool, ABC):
    overwrite = True
    linux_mode = True
    linux_header = f'# -*- coding: utf-8 -*-\n'
