# -*- coding: utf-8 -*-
import abc as _abc
import argparse as _argparse
import os as _os
import pathlib as _pathlib
import typing as _typing

import jinja2 as _jinja2


class BaseTool(_abc.ABC):
    def __init__(
            self,
            path: _typing.Union[_pathlib.Path, str],
            lib_path: _typing.Union[_pathlib.Path, str],
            args: _argparse.Namespace,
            version: str
    ) -> None:
        self.path: _pathlib.Path = path if isinstance(path, _pathlib.Path) else _pathlib.Path(path)
        self.lib_path: _pathlib.Path = lib_path if isinstance(lib_path, _pathlib.Path) else _pathlib.Path(lib_path)
        self.args: _argparse.Namespace = args
        self.version: str = version

    @_abc.abstractmethod
    def __call__(self) -> None:
        pass

    def _build_template(
            self,
            template_path: _pathlib.Path,
            source_path: _pathlib.Path,
    ) -> None:
        self._create_level(template_path=template_path, source_path=source_path)
        self._create_files(template_path=template_path, source_path=source_path)

    def _create_level(
            self,
            template_path: _pathlib.Path,
            source_path: _pathlib.Path
    ) -> None:
        for entity in _os.listdir(template_path):
            clean = self._clear_entity(entity)

            if not clean:
                continue

            if clean in self._excluded_level:
                continue

            if '.' in clean and clean not in self._included_level:
                continue

            if not _os.path.exists(source_path / clean):
                _os.makedirs(source_path / clean)

            self._create_level(template_path / entity, source_path / clean)

    def _create_files(
            self,
            template_path: _pathlib.Path,
            source_path: _pathlib.Path
    ) -> None:
        for entity in _os.listdir(template_path):
            clean = self._clear_entity(entity)

            if not clean or clean in self._excluded_files:
                continue

            if clean in self._included_files or any([clean.endswith(el) for el in ('.py',)]):
                if _os.path.isfile(source_path / clean):
                    continue

                template = _jinja2.Environment(loader=_jinja2.FileSystemLoader(template_path)).get_template(entity)

                with open(source_path / clean, mode="w", encoding="utf-8") as f:
                    f.write(template.render(**self._render_data))

            elif '.' in entity:
                continue

            else:
                self._create_files(template_path / entity, source_path / clean)

    def _clear_entity(self, entity: str) -> _typing.Optional[str]:
        if not entity.endswith('-tpl'):
            return None

        clean = entity.replace('-tpl', '')

        for key, value in self._clear_data.items():
            if not clean.startswith(f'{{{key}}}'):
                continue

            clean = clean.replace(f'{{{key}}}', value)
            break

        return clean

    @property
    def _render_data(self) -> _typing.Dict[str, _typing.Any]:
        """
        For example: {'test': 'some input'} will use 'some input' value in jinja fields and functions like {{ test }}.
        """
        return {}

    @property
    def _clear_data(self) -> _typing.Dict[str, str]:
        """
        For example: {'template': 'test'} will create 'test' file or directory from '{template}-tpl'.
        """
        return {}

    @property
    def _included_files(self) -> _typing.List[str]:
        return []

    @property
    def _excluded_files(self) -> _typing.List[str]:
        return []

    @property
    def _included_level(self) -> _typing.List[str]:
        return []

    @property
    def _excluded_level(self) -> _typing.List[str]:
        return []
