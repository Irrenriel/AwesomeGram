# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC


class AbstractTool(ABC):
    @abstractmethod
    def __init__(self, path):
        pass

    @abstractmethod
    def on_process(self):
        pass
