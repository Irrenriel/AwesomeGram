# -*- coding: utf-8 -*-
import logging
import os

from yaml import load

from resources.utils.base.exceptions import ModulesNotCreated
from resources.utils.localizator.exceptions import LangNotFound, TextNotFound

try:
    from yaml import CLoader as Loader

except ImportError:
    from yaml import Loader


class Locale:
    def __init__(self, lang: str, values: dict):
        self.lang = lang
        self.__values = values

    def get(self, key: str, **kwargs):
        try:
            pattern_text = self.extract_groups(self.__values, key.split('.'))

        except KeyError:
            return

        result = None
        error_kwargs = []

        while True:
            try:
                result = pattern_text.format(**{k: str(v) for k, v in kwargs.items()})

            except KeyError as e:
                for arg in e.args:
                    kwargs[arg] = f"{{{arg}}}"
                    error_kwargs.append(arg)

            finally:
                if error_kwargs:
                    logging.error(f'Not enough arguments for "{result}": {", ".join(error_kwargs)}')

                return result

    def extract_groups(self, values: dict, groups: list):
        if groups:
            return self.extract_groups(values[groups.pop(0)], groups)

        return values


class LocaleManager:
    locales = {}
    default_locale = None

    modules_dir = 'modules'

    @classmethod
    def set_default_locale(cls, lang: str):
        cls.default_locale = lang

    @classmethod
    def initialize_new_locales(cls, path):
        modules_path = path / cls.modules_dir

        if not os.path.exists(modules_path):
            raise ModulesNotCreated(cls.modules_dir)

        avail_modules = [m for m in os.listdir(modules_path) if '.' not in m]

        if not avail_modules:
            raise ModulesNotCreated(cls.modules_dir)

        logging.info(f'Successfully found {len(avail_modules)} modules for LocaleManager!')

        for module in avail_modules:
            module_path = path / 'resources' / module
            locales_path = module_path / 'locales'

            if not os.path.exists(module_path) or not os.path.exists(locales_path):
                logging.error(f'No directory for module "{module}" in resources folder. Skipped!')
                continue

            avail_locales = [l for l in os.listdir(locales_path) if l.endswith('.yml')]

            if not avail_locales:
                logging.error(f'No available locales for module "{module}"')
                continue

            for locale in avail_locales:
                with open(locales_path / locale, "r", encoding="utf-8") as f:
                    lang = locale.replace('.yml', '', 1)
                    values = load(f, Loader)

                    cls.locales.setdefault(lang, []).append(Locale(lang, values))

                logging.info(f'Successfully installed "{locale}" locale from "{module}" module.')

        logging.info(f"Now available {len(cls.locales)} locales: {', '.join([f'{i}' for i in cls.locales])}.")

    @classmethod
    def get(cls, lang: str, key: str, **kwargs):
        locale = cls.locales.get(lang)

        if not locale:
            if lang == cls.default_locale:
                raise LangNotFound

            return cls.get(cls.default_locale, key, **kwargs)

        text = None

        for l in locale:
            temp = l.get(key, **kwargs)

            if not temp:
                continue

            text = temp

        if text is None:
            raise TextNotFound

        return text
