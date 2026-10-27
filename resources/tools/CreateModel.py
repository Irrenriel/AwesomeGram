# -*- coding: utf-8 -*-
import re
from string import punctuation
from typing import List

from loguru import logger

from resources.base.core import DirectoriesAndFilesChecking
from resources.tools.core import CustomTool
from resources.tools.exceptions import InvalidModelName, UnknownColumnOption, UnknownColumnType


class CreateModel(CustomTool):
    _AVAILABLE_SIMPLE_TYPES = {
        'text': "TEXT",
        'int': "INT",
        'integer': "INT",
        'bigint': "BIGINT",
        'datetime': "DateTime",
        'boolean': "BOOLEAN",
        'bool': "BOOLEAN"
    }
    _AVAILABLE_OPTS = {
        'primary': ', primary_key=True',
        'primary_key': ', primary_key=True',
        'nullable': ', nullable=True',
        'null': ', nullable=True',
        'notnull': ', nullable=False',
        'not_null': ', nullable=False',
        'notnullable': ', nullable=False',
        'not_nullable': ', nullable=False',
    }

    _BASE_IMPORTS = set()
    _ALCHEMY_IMPORTS = set()
    _OTHER_IMPORTS = set()

    __model_name = None
    __file_name = None

    _template_model_name = 'model_name'
    _content = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if any([ch in self._model_name for ch in punctuation]):
            raise InvalidModelName

        if len(self._model_name) > 64:
            raise InvalidModelName

    def on_process(self):
        """
        Structure:

        < ROOT >
            ⊳ resources
                ⊳ models
                    ⊳ tables
                        ⊳ <YOUR_NEW_MODEL>

        """
        DirectoriesAndFilesChecking(
            [
                self.path / 'modules',
                self.path / 'resources',
                self.path / 'modules' / 'config.py',
                self.path / 'core' / 'database',
                self.path / 'resources' / 'models' / 'tables' / '__init__.py'
            ]
        )

        self._create_content()

        template_path = self.path / 'resources' / 'tools' / 'templates' / 'create_model_templates'

        self._creating_files(template_path, self.path)

        logger.info(f'Successfully created model with "{self._file_name}" file!')

    def _create_content(self):
        self._ALCHEMY_IMPORTS.add('Column')

        pattern = '{var} = Column("{var}", {type}{opt})'

        for arg in self.argv_data.content[1:]:
            var, t, opt = self._prepare_values(arg.lower().split(':'))

            match var:
                case 'id':
                    if not t:
                        t = 'INT'

                    self._ALCHEMY_IMPORTS.add(t)

                case 'language':
                    if not t:
                        t = 'Enum(Languages)'

                    self._ALCHEMY_IMPORTS.add('Enum')
                    self._OTHER_IMPORTS.add('from resources.models.enums import Languages')

                case 'created_at' | 'updated_at' | 'deleted_at' | 'banned_at' | 'banned_until':
                    if not t:
                        t = 'DateTime'

                    self._ALCHEMY_IMPORTS.add(t)

                case 'is_deleted' | 'is_banned':
                    if not t:
                        t = 'BOOLEAN'

                    self._ALCHEMY_IMPORTS.add(t)

            self._content.append(pattern.format(var=var, type=t, opt=opt))

    def _prepare_values(self, args: List[str]) -> tuple:
        l_args = len(args)
        var, t, opt = args[0], '', ''

        if l_args == 2:
            if not (t := self._set_type(args[1], set_opt=True)):
                opt = self._set_opt(args[1])

        elif l_args == 3:
            t = self._set_type(args[1])
            opt = self._set_opt(args[2])

        return var, t, opt

    def _set_type(self, arg, set_opt: bool = False):
        if arg in self._AVAILABLE_SIMPLE_TYPES:
            self._ALCHEMY_IMPORTS.add(
                t := self._AVAILABLE_SIMPLE_TYPES.get(arg)
            )
            return t

        if arg in ('lang', 'language'):
            self._OTHER_IMPORTS.add('from resources.models.enums import Languages')
            self._ALCHEMY_IMPORTS.add('Enum')
            return 'Enum(Languages)'

        if not set_opt:
            raise UnknownColumnType(arg, [*self._AVAILABLE_SIMPLE_TYPES, 'lang', 'language'])

    def _set_opt(self, arg):
        if arg in self._AVAILABLE_OPTS:
            return self._AVAILABLE_OPTS.get(arg)

        match arg:
            case 'utc':
                self._BASE_IMPORTS.add('from datetime import datetime, UTC')
                # lambda: evaluated on each insert, not once at import
                return ', default=lambda: datetime.now(UTC)'

            case 'true':
                return ', default=True'

            case 'false':
                return ', default=False'

            case 'language':
                self._OTHER_IMPORTS.add('from resources.models.enums import Languages')
                return ', default=Languages.EN'

            case 'en':
                self._OTHER_IMPORTS.add('from resources.models.enums import Languages')
                return ', default=Languages.EN'

        raise UnknownColumnOption(arg, [*self._AVAILABLE_OPTS, 'utc', 'true', 'false', 'language', 'en'])

    def _clear_name(self, ent: str):
        if not ent.endswith('-tpl'):
            return

        clean = ent.replace('-tpl', '')

        if not self._template_model_name:
            return clean

        if clean.startswith(self._template_model_name):
            clean = clean.replace(self._template_model_name, self._file_name)

        return clean

    @property
    def _model_name(self):
        if not self.__model_name:
            name = self.argv_data.content[0].title()

            if name.endswith('Model'):
                self.__model_name = name

            elif name.lower().endswith('model'):
                self.__model_name = "Model".join(name.rsplit('model', 1))

            else:
                self.__model_name = f'{name}Model'

        return self.__model_name

    @property
    def _file_name(self):
        if not self.__file_name:
            self.__file_name = re.sub(r'(?<!^)(?=[A-Z])', '_', self._model_name).lower()

        return self.__file_name

    @property
    def _data(self):
        return {
            'header': self.linux_header,
            'model_name': self._model_name,
            'table_name': ''.join(self._file_name.rsplit('_model', 1)),
            'content': self._content,
            'imports': self._imports,
        }

    @property
    def _imports(self):
        return f'''\
{'\n'.join(self._BASE_IMPORTS) + '\n\n' if self._BASE_IMPORTS else ''}\
from sqlalchemy import {', '.join(self._ALCHEMY_IMPORTS)}

from core.database.db import Base  # Change import to the right file
{'\n'.join(self._OTHER_IMPORTS) if self._OTHER_IMPORTS else ''}\
'''
