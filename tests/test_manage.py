# -*- coding: utf-8 -*-
"""
Smoke tests for manage.py: every command runs on a fresh copy of the repository
and the generated files at least compile.

Run: pip install -r requirements.txt pytest && python -m pytest tests
"""
import py_compile
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def project(tmp_path: Path) -> Path:
    # A dot in the path on purpose: it used to break file/directory checks
    dst = tmp_path / 'my.bot'
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns('.git', 'tests', '__pycache__', 'venv', '.venv'))
    return dst


def manage(project: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, 'manage.py', *args], cwd=project, capture_output=True, text=True, timeout=60
    )


def assert_ok(result: subprocess.CompletedProcess):
    assert result.returncode == 0, result.stderr
    assert 'Traceback' not in result.stderr, result.stderr


def assert_compiles(*files: Path):
    for file in files:
        py_compile.compile(str(file), doraise=True)


def test_help_lists_all_commands(project):
    result = manage(project, '--help')

    assert_ok(result)
    for command in ('--create-module', '--create-app', '--init-db', '--create-model'):
        assert command in result.stderr


def test_create_module_without_name_fails_with_clear_error(project):
    result = manage(project, '--create-module')

    assert result.returncode != 0
    assert 'ArgumentValueNotFound' in result.stderr


def test_create_modules_and_app(project):
    assert_ok(manage(project, '--create-module', 'first'))
    (project / 'modules' / '__pycache__').mkdir()  # appears after any import of modules.config
    assert_ok(manage(project, '--create-module', 'second'))
    assert_ok(manage(project, '--create-app'))

    installing = (project / 'modules' / 'installing.py').read_text(encoding='utf-8')
    assert 'install_first_handlers' in installing and 'install_second_handlers' in installing
    assert '__pycache__' not in installing
    assert "default_locale = 'EN'" in (project / 'app.py').read_text(encoding='utf-8')
    assert (project / 'resources' / 'locales' / 'en.yml').is_file()
    assert_compiles(
        project / 'app.py',
        project / 'modules' / 'installing.py',
        project / 'modules' / 'first' / 'handlers.py',
        project / 'resources' / 'middlewares' / 'main_middleware.py',
    )


@pytest.mark.parametrize('async_mode', ['false', 'true'])
def test_init_db(project, async_mode):
    assert_ok(manage(project, '--create-module', 'first'))

    assert_ok(manage(project, '--init-db', f'async={async_mode}'))

    assert_compiles(project / 'core' / 'database' / 'db.py')


def test_create_model(project):
    assert_ok(manage(project, '--create-module', 'first'))
    assert_ok(manage(project, '--init-db'))

    result = manage(project, '--create-model', 'user', 'id:int:primary', 'name:text:null', 'created_at:datetime:utc')

    assert_ok(result)
    model = project / 'resources' / 'models' / 'tables' / 'user_model.py'
    assert_compiles(model)
    assert 'default=lambda: datetime.now(UTC)' in model.read_text(encoding='utf-8')


@pytest.mark.parametrize(
    ('field', 'error'),
    [('name:varchar:null', 'UnknownColumnType'), ('name:text:uniq', 'UnknownColumnOption')],
)
def test_create_model_rejects_unknown_type_and_option(project, field, error):
    assert_ok(manage(project, '--create-module', 'first'))
    assert_ok(manage(project, '--init-db'))

    result = manage(project, '--create-model', 'user', 'id:int:primary', field)

    assert result.returncode != 0
    assert error in result.stderr
