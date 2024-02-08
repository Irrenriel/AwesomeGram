# -*- coding: utf-8 -*-
import os
from typing import Union, List

from aiogram import F
from loguru import logger

try:
    from yaml import CLoader as Loader, load

except ImportError:
    from yaml import Loader, load

from resources.base.exceptions import LangNotFound


class Locale:
    def __init__(self, values: dict, *args, **kwargs):
        self.__values = values

    def __call__(self, key: str, *args, **kwargs):
        try:
            pattern_text = self.extract_groups(self.__values, key.split('.'))

        except KeyError as e:
            logger.error(f'Can not find pattern by "{e.args[0]}" key in "{key}".')
            return key

        error_kwargs = []

        while True:
            try:
                result = pattern_text.format(**{k: str(v) for k, v in kwargs.items()})

            except KeyError as e:
                for arg in e.args:
                    kwargs[arg] = f"{{{arg}}}"
                    error_kwargs.append(arg)

                continue

            if error_kwargs:
                logger.error(f'Not enough arguments for "{result}": {", ".join(error_kwargs)}')

            return result

    def extract_groups(self, values: dict, groups: list):
        if groups:
            return self.extract_groups(values[groups.pop(0)], groups)

        return values


class LocalesManager:
    # Pool of languages:
    _LOCALES = {}

    # Modules directory name:
    _LOCALES_PATH = "resources/locales/"

    # Default locale:
    default_locale = None

    @classmethod
    def init(cls, path, *args, **kwargs):
        locales_path = path / cls._LOCALES_PATH

        if not os.path.exists(locales_path):
            logger.error('No locales directory in resources folder!')
            return

        available_locales = [l for l in os.listdir(locales_path) if l.endswith('.yml')]

        if not available_locales:
            logger.error(
                'There are no available locales in the directory for localization installation!'
            )
            return

        for locale in available_locales:
            with open(locales_path / locale, "r", encoding="utf-8") as f:
                values = load(f, Loader)

            lang = locale.replace('.yml', '', 1)
            cls._LOCALES[lang.upper()] = Locale(values)

            logger.info(f'Localization "{locale}" installed successfully!')

        list_locales = ", ".join([f'"{i}"' for i in cls._LOCALES])
        logger.info(f'Now available {len(cls._LOCALES)} locales: {list_locales}.')

    @classmethod
    def get(cls, key: str, lang: str = default_locale, *args, **kwargs) -> str:
        locale = cls._LOCALES.get(lang)

        if not locale:
            if lang == cls.default_locale:
                raise LangNotFound

            return cls.get(key, lang=cls.default_locale, *args, **kwargs)

        return locale(key, *args, **kwargs)

    @classmethod
    def text(cls, key: str, lang: str = default_locale, *args, **kwargs) -> str:
        return cls.get(f'text.{key}', lang, *args, **kwargs)

    @classmethod
    def button(cls, key: str, lang: str = default_locale, *args, **kwargs) -> str:
        return cls.get(f'button.{key}', lang, *args, **kwargs)

    @classmethod
    def handler_buttons(cls, key: str) -> List[str]:
        return F.text.in_([cls.button(key, lang) for lang in cls._LOCALES.keys()])
