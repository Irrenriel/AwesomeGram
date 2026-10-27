# -*- coding: utf-8 -*-
import argparse as _argparse
import keyword as _keyword
import typing as _typing

from .BaseTool import BaseTool


class StartProject(BaseTool):
    def __call__(self, *args, **kwargs) -> None:
        self._build_template(
            template_path=self.lib_path / "templates" / "start-project",
            source_path=self.path,
        )

        print(f'Successfully created project "{self.args.name.lower()}"!')

    @classmethod
    def project_name_check(cls, value: str):
        if value.isdigit():
            raise _argparse.ArgumentTypeError('Project name must be a string!')

        if len(value) < 6 or len(value) > 32:
            raise _argparse.ArgumentTypeError('Project name must be between 6 and 32 characters!')

        # The project directory is imported as a Python package, so the name must be a valid identifier:
        if not value.lower().isidentifier() or _keyword.iskeyword(value.lower()):
            raise _argparse.ArgumentTypeError(
                'Project name may contain only letters, digits and "_", must not start with a digit '
                'and must not be a Python keyword!'
            )

        return value

    @property
    def _clear_data(self) -> _typing.Dict[str, str]:
        return {
            'project_name': self.args.name.lower(),
        }

    @property
    def _render_data(self) -> _typing.Dict[str, _typing.Any]:
        return {
            'version': self.version,
        }

    @property
    def _included_files(self) -> _typing.List[str]:
        return [
            'Dockerfile',
            '.env.example',
            '.gitignore',
        ]

    @property
    def _excluded_level(self) -> _typing.List[str]:
        return [
            'Dockerfile',
        ]
